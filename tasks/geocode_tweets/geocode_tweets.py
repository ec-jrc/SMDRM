import json
import logging
import pandas
import os
import sys
import typing

from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.common import iter_in_batches, get_version, path_arg, log_execution
from libdrm.pipelines import Pipeline

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("geocode_tweets")
# root dir
root_dir = os.path.dirname(os.path.abspath(__file__))


def load_global_places() -> pandas.DataFrame:
    """Load Global Places Gazetier as Pandas DataFrame."""
    places_df = pandas.read_csv(
        os.path.join(root_dir, "config/global_places_v1.tsv"), sep="\t"
    )
    # enforce int type for region id
    places_df.region_id = places_df.region_id.astype(int)
    return places_df


def filter_places_by_bbox(
    places_df: pandas.DataFrame,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> pandas.Series:
    """Filter places within a given bounding box."""
    within_mask = places_df.apply(
        lambda city: min_lon <= city.longitude <= max_lon
        and min_lat <= city.latitude <= max_lat,
        axis=1,
    )
    return places_df[within_mask].copy()


def filter_places_by_region_id(
    region_id: int,
    places_df: pandas.DataFrame,
) -> pandas.DataFrame:
    """Filter places for the given region ID."""
    filtered_places_df = places_df[places_df.region_id == region_id].copy()
    if filtered_places_df.empty:
        raise ValueError("Region ID must exists in the Global Places dataset.")
    return filtered_places_df


def get_bbox_centroid(bbox: str, precision: int = 6) -> tuple:
    """Compute bounding box centroid (lat, lon)
    coordinates using minimun and maximum coordinates."""
    min_lon, min_lat, max_lon, max_lat = bbox.split(",")
    latitude = (float(min_lat) + float(max_lat)) / 2
    longitude = (float(min_lon) + float(max_lon)) / 2
    return round(latitude, precision), round(longitude, precision)


def get_gpes(datapoint: dict, min_len: int = 4) -> list:
    """Get Geo Political Entities from place candidates if any."""
    try:
        return [
            gpe
            for gpe in datapoint["place"]["candidates"]["GPE"]
            if len(gpe) >= min_len
        ]
    except (KeyError, TypeError):
        return []


def flatten_gpes(gpes: typing.List[str]) -> typing.List[str]:
    """Decompone each (space separated) GPE place candidate
    into a unique entity to increase matching chances."""
    return [entity for gpe in gpes for entity in gpe.split(" ")]


def get_city_filter(
    places_df: pandas.DataFrame, gpes: typing.List[str]
) -> pandas.Series:
    """Pandas boolean mask of matching cities in Global Places against the given GPEs."""
    return places_df.city_name.isin(gpes) & places_df.city_alternatenames.str.contains(
        "|".join(gpes), na=False, case=False, regex=True
    )


def get_region_filter(
    places_df: pandas.DataFrame, gpes: typing.List[str]
) -> pandas.Series:
    """Pandas boolean mask of matching regions in Global Places against the given GPEs."""
    return places_df.region_name.isin(gpes) | places_df.subregion_name.isin(gpes)


def geocode_datapoints(
    datapoints: typing.Iterable[dict],
    places_df: pandas.DataFrame,
) -> typing.Iterable[dict]:
    """Enrich datapoints with extracted place metadata.
    Return match(es) between datapoint GPE place candidates and (filtered) Global Places."""
    for datapoint in datapoints:

        # Geo Political Entities found at transform_tweet task
        # keep gpes with at least min_len characters
        gpes = flatten_gpes(get_gpes(datapoint, min_len=3))

        if not gpes:
            # cannot geocode without GPEs
            yield datapoint
            continue

        # show GPEs to use for geocoding
        console.debug("GPEs={}".format(gpes))

        # add placeholder fields
        datapoint["place"]["meta"] = []

        # try matching cities
        # TODO: convert to testable functions
        matches = get_city_filter(places_df, gpes)
        hits = matches.sum()
        console.debug("city matches={}".format(hits))

        if hits == 0:
            # try matching regions if match_cities is empty
            console.debug(
                "GPEs do not match any city in Global Places. Try matching regions..."
            )
            matches = get_region_filter(places_df, gpes)

            fields = [
                "country_name",
                "country_code",
                "region_name",
                "bbox",
                "region_id",
            ]
            df = places_df[matches][fields]
            df.drop_duplicates(inplace=True)
            matches = len(df)
            console.debug("region matches={}".format(matches))

            if matches == 0:
                console.debug("Geocode failed to find Global Places for this datapoint")
                yield datapoint
                continue

            # compute centroid latitude and longitude coordinates from bbox
            centroid = df.bbox.apply(get_bbox_centroid)
            df["latitude"] = centroid.map(lambda c: c[0])
            df["longitude"] = centroid.map(lambda c: c[1])
            df.drop(columns="bbox", inplace=True)

        else:
            fields = [
                "country_name",
                "country_code",
                "region_name",
                "city_name",
                "latitude",
                "longitude",
                "region_id",
            ]
            df = places_df[matches][fields]

        # update geocode output fields
        datapoint["place"]["meta"] = df.to_dict(orient="records")

        yield datapoint


def task_metrics(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]:
    """Collect task metrics."""
    total = 0
    with_gpe = 0
    geolocated = 0
    geolocated_fuzzy = 0
    for datapoint in datapoints:
        total += 1
        if get_gpes(datapoint):
            with_gpe += 1
        meta = datapoint["place"].get("meta")
        if meta:
            geolocated += 1
            if len(meta) > 1:
                geolocated_fuzzy += 1
        yield datapoint
    console.info(
        dict(
            total=total,
            with_gpe=with_gpe,
            geolocated=geolocated,
            geolocated_fuzzy=geolocated_fuzzy,
        )
    )


def log_datapoints(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]:
    """Log processed datapoints."""
    for datapoint in datapoints:
        console.debug(datapoint)
        yield datapoint


def make_ndjson_batches(
    datapoints: typing.Iterable[dict],
    batch_size: int = 1000,
) -> typing.Iterable[str]:
    """Iterate NDJSON batches from a generator of JSON datapoints."""
    for batch in iter_in_batches(datapoints, batch_size=batch_size):
        yield "".join(
            [json.dumps(datapoint, ensure_ascii=False) + "\n" for datapoint in batch]
        )


@log_execution(console)
def run(args):
    console.info("opts={}...".format(vars(args)))
    if args.debug:
        console.setLevel(logging.DEBUG)

    if not args.region_id and not all(
        [args.min_lon, args.min_lat, args.max_lon, args.max_lat]
    ):
        console.warning(
            "Neither region ID not bounding box filters were given. Geocoding precision will be low."
        )

    # make output path
    if not args.output_path:
        args.output_path = args.input_path.replace(".zip", "_geo.zip")
        console.warning("Default output path is {}".format(args.output_path))

    # input path validation
    zip_file = ZipFileModel(args.input_path)
    if not zip_file.is_valid():
        console.error("Not a valid zip file.")
        sys.exit(13)

    # load global places dataset
    places_df = load_global_places()

    if args.region_id:
        # filter only places of interest wrt the region identifier linked to the collection
        console.info("filter global places by region ID: {}".format(args.region_id))
        places_df = filter_places_by_region_id(args.region_id, places_df)

    if all([args.min_lon, args.min_lat, args.max_lon, args.max_lat]):
        # filter only places of interest wrt the region bounding box linked to the collection
        console.info(
            "filter global places by bbox: {}".format(
                ",".join([args.min_lon, args.min_lat, args.max_lon, args.max_lat])
            )
        )
        places_df = filter_places_by_bbox(
            places_df, args.min_lon, args.min_lat, args.max_lon, args.max_lat
        )

    # build geocode pipeline
    geocode_pipeline = Pipeline()
    geocode_pipeline.add(geocode_datapoints, dict(places_df=places_df))
    geocode_pipeline.add(task_metrics)
    geocode_pipeline.add(log_datapoints)
    geocode_pipeline.add(make_ndjson_batches, dict(batch_size=args.batch_size))

    # execute pipeline on annotated datapoints
    datapoints = zip_file.iter_jsonl()
    geocoded_datapoints = geocode_pipeline.execute(datapoints)

    # cache
    zip_file.cache(args.output_path, geocoded_datapoints)


if __name__ == "__main__":
    """
    Exit Codes
      11 - Path not found
      12 - Path is a directory, but a zip file is expected
      13 - Not a valid zip file
    """

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Match place candidates with our Global Regions/Cities datasets."
    )
    parser.add_argument(
        "--input-path",
        required=True,
        type=path_arg,
        help="path from which you want to get input data.",
    )
    parser.add_argument(
        "--output-path",
        default=False,
        help="path to which you want to save the task output.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="size of each batch in which a file is split. Default is %(default)d.",
    )
    parser.add_argument(
        "--min-lon",
        required=False,
        type=float,
        help="minimum longitude of the bounding box of the area under scrutiny.",
    )
    parser.add_argument(
        "--min-lat",
        required=False,
        type=float,
        help="minimum latitude of the bounding box of the area under scrutiny.",
    )
    parser.add_argument(
        "--max-lon",
        required=False,
        type=float,
        help="maximum longitude of the bounding box of the area under scrutiny.",
    )
    parser.add_argument(
        "--max-lat",
        required=False,
        type=float,
        help="maximum latitude of the bounding box of the area under scrutiny.",
    )
    parser.add_argument(
        "--region-id",
        required=False,
        type=int,
        help="region ID that triggered the task.",
    )
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())
