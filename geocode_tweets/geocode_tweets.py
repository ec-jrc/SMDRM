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


class Place:
    """Class representation of a geo localized place."""

    def __init__(
        self,
        region_id: int = None,
        latitude: float = None,
        longitude: float = None,
        name: str = None,
        type: str = None,
    ):
        self.region_id = region_id
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.type = type

    def __str__(self):
        return str(self.asdict())

    def serialize(self):
        # to dictionary
        return vars(self)


def load_global_places():
    places_df = pandas.read_csv(
        os.path.join(root_dir, "config/global_places_v1.tsv"), sep="\t"
    )
    places_df.region_id = places_df.region_id.astype(int)
    return places_df


def filter_places_by_region_id(
    region_id: int,
    places_df: pandas.DataFrame,
) -> pandas.DataFrame:
    # filter only places of interest (wrt the region associated with the collection)
    filtered_places_df = places_df[places_df.region_id == region_id]
    if filtered_places_df.empty:
        raise ValueError("Region ID must exists in the Global Locations dataset.")
    return filtered_places_df


def make_place_reference_key(places_df: pandas.DataFrame) -> pandas.Series:
    """Concatenate place names into a single string.
    This enables to verify if the string contains the place candidates."""
    return (
        places_df.city_name
        + ","
        + places_df.city_asciiname
        + ","
        + places_df.city_alternatenames
        + ","
        + places_df.country_name
        + ","
        + places_df.region_name
        + ","
        + places_df.subregion_name
    )


def make_place_candidate_match_mask(
    gpe: str,
    reference_keywords: pandas.Series,
) -> pandas.Series:
    """Boolean mask of matches of the GPE place candidate pattern
    contained in the reference keywords (i.e. contains)."""
    # decompose GPE place candidate into a substring regex pattern to verify
    # if the reference keywords contain any of the place candidate substrings
    return reference_keywords.str.contains(
        "|".join(gpe.split(" ")), case=False, regex=True
    )


def get_bbox_centroid(bbox: str) -> tuple:
    """Compute bounding box centroid (lat, lon)
    coordinates using minimun and maximum coordinates."""
    min_lon, min_lat, max_lon, max_lat = bbox.split(",")
    y = (float(min_lat) + float(max_lat)) / 2
    x = (float(min_lon) + float(max_lon)) / 2
    return y, x


def get_gpes(datapoint: dict) -> list:
    """Get Geo Political Entities from place candidates if any."""
    gpes=None
    try:
        gpes = datapoint["place"]["candidates"]["GPE"]
    except TypeError as te:
        console.warning(te)
    finally:
        return gpes


def geocode(
    gpes: typing.List[str],
    region_id: int,
    places_df: pandas.DataFrame,
) -> typing.Type[Place]:
    """Return the first GPE (place candidate) that matches Global Places filtered by region ID."""

    # make reference keywords key to evaluate it contains a given gpe
    ref_keywords = make_place_reference_key(places_df)

    # Geo Political Entities found at transform_tweet task
    for gpe in gpes:

        # skip short placename like 'US', 'UK'
        if len(gpe) < 3:
            continue

        # increase matching chances by taking sub-string of the place candidate
        matches_mask = make_place_candidate_match_mask(gpe, ref_keywords)
        n_geolocated_places = matches_mask.sum()
        console.debug("gpe={} {} matches found".format(gpe, n_geolocated_places))

        # get the first match
        candidate = places_df.loc[matches_mask.idxmax()]

        # use the city coords if only 1 match
        # use the region centroid coords using the bbox if multiple matches
        if n_geolocated_places == 0:
            console.debug("no match found")
            continue

        elif n_geolocated_places == 1:
            city_yx = (candidate.latitude, candidate.longitude)
            console.debug("using city (latlon) coords")
            # this datapoint will be geolocated at city level
            return Place(
                region_id=region_id,
                latitude=candidate.latitude,
                longitude=candidate.longitude,
                name=candidate.city_name,
                type="city",
            ).serialize()

        elif n_geolocated_places > 1:
            # multiple cities matched
            # might indicate datapoint refers to region
            # compute bbox centroid as common place coordinates
            latitude, longitude = get_bbox_centroid(candidate.bbox)
            console.debug("using region centroids (latlon) coords")
            # this datapoint will be geolocated at region level
            # thus, it is optional to check the other place candidates
            return Place(
                region_id=region_id,
                latitude=latitude,
                longitude=longitude,
                name=candidate.subregion_name or candidate.region_name,
                type="centroid",
            ).serialize()
        else:
            console.warning("not possible")


def geocode_datapoints_with_gpes(
    datapoints: typing.Iterable[dict],
    region_id: int,
    places_df: pandas.DataFrame,
) -> typing.Iterable[dict]:
    """Generate geocoded datapoints to be writte to file"""
    for datapoint in datapoints:
        # get gpes from place field
        gpes = get_gpes(datapoint)
        if gpes:
            place_meta = geocode(gpes, region_id, places_df)
            if place_meta:
                datapoint["place"].update(place_meta)

        yield datapoint


def task_metrics(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]:
    """Collect task metrics."""
    total=0
    with_gpe=0
    geolocated=0
    for datapoint in datapoints:
        total += 1
        if get_gpes(datapoint):
            with_gpe += 1
        if "region_id" in datapoint["place"]:
            geolocated += 1
        yield datapoint
    console.info(dict(total=total, with_gpe=with_gpe, geolocated=geolocated))


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

    if not args.region_id:
        console.warning("Without region ID the quality of geocode is substantially lower.")

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
    # replace NaN with empty string
    places_df.fillna("", inplace=True)

    if args.region_id:
        # filter only places of interest wrt the region associated to the collection
        places_df = filter_places_by_region_id(args.region_id, places_df)

    # build geocode pipeline
    geocode_pipeline = Pipeline()
    geocode_pipeline.add(geocode_datapoints_with_gpes, dict(region_id=args.region_id, places_df=places_df))
    geocode_pipeline.add(task_metrics)
    geocode_pipeline.add(log_datapoints)
    geocode_pipeline.add(make_ndjson_batches)

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
        help="The path from which you want to get input data.",
    )
    parser.add_argument(
        "--output-path",
        default=False,
        type=path_arg,
        help="The path to which you want to save the task output.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="The size of each batch in which a file is split.",
    )
    parser.add_argument(
        "--region-id",
        required=False,
        type=int,
        help="The region ID that triggered the task.",
    )
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())
