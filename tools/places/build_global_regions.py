import glob
import json
import os
import typing


# the directory of this file
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
# input data dir must exist
input_data_dir = os.path.join(root, "inputs")
if not os.path.isdir(input_data_dir):
    raise OSError("Input data directory not found.")

# output data can be created if not found
output_data_dir = os.path.join(root, "outputs")
os.makedirs(output_data_dir, exist_ok=True)

# with version
filename = "global_regions_v1"


def parse_bbox(bbox: list):
    # bbox list order: min_lon, max_lon, min_lat, max_lat
    return ",".join(["{:.6f}".format(round(float(coord), 6)) for coord in bbox])


def iter_geo_features(input_path: str) -> typing.Iterable[dict]:

    with open(input_path) as infile:
        # load data
        geo = json.load(infile)

        # process raw features
        for feature in geo["features"]:
            # parse required fields from properties

            # country ISO 3166 alpha3 is always GID_O
            country_a3 = feature["properties"]["GID_0"]
            country_name = feature["properties"]["NAME_0"]
            # available only on levels above 0
            region_name = feature["properties"].get("NAME_1", None)
            subregion_name = feature["properties"].get("NAME_2", None)
            region_name_local = feature["properties"].get("NL_NAME_1", None) or feature["properties"].get("NL_NAME_2", None)

            # add bbox as field
            bbox = parse_bbox(feature["bbox"])

            # replace properties dict
            feature["properties"] = dict(
                country_a3=country_a3,
                country_name=country_name,
                region_name=region_name,
                subregion_name=subregion_name,
                region_name_local=region_name_local,
                bbox=bbox,
            )

            # remove bbox field
            del feature["bbox"]

            # add to global regions
            yield feature


def make_geojson(test: bool = False) -> dict:
    # features placeholder
    geojson = {
        "type": "FeatureCollection",
        "name": filename,
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }


    # used as region id
    feature_id = 1

    # get input paths
    input_paths = glob.iglob(os.path.join(input_data_dir, "*.geojson"))

    for path in input_paths:
        print("processing", path)

        # generate features
        for feature in iter_geo_features(path):

            # add region id
            feature["properties"]["region_id"] = feature_id

            # append to global geojson
            geojson["features"].append(feature)
            feature_id += 1

            # break after first iteration
            if test:
                del feature["geometry"]
                print(feature)
                print()
                break

    if not geojson["features"]:
        raise OSError("Empty geojson features list. Check {}".format(input_data_dir))

    return geojson


def save_geojson(data: dict) -> None:
    # save to json file
    filepath = os.path.join(output_data_dir, "{}.geojson".format(filename))
    print("saving to", filepath)
    with open(filepath, "w", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Build Global Regions basemap.")
    parser.add_argument("--test", action="store_true", default=False, help="Enable tests.")
    args = parser.parse_args()
    # buils global regions
    geojson = make_geojson(args.test)
    # save geojson file
    if not args.test:
        save_geojson(geojson)
