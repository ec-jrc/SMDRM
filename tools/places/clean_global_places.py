"""
# Datamodel

    The main 'geoname' table has the following fields :
    ---------------------------------------------------
    geonameid         : integer id of record in geonames database
    name              : name of geographical point (utf8) varchar(200)
    asciiname         : name of geographical point in plain ascii characters, varchar(200)
    alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
    latitude          : latitude in decimal degrees (wgs84)
    longitude         : longitude in decimal degrees (wgs84)
    feature class     : see http://www.geonames.org/export/codes.html, char(1)
    feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
    country code      : ISO-3166 2-letter country code, 2 characters
    cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
    admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
    admin3 code       : code for third level administrative division, varchar(20)
    admin4 code       : code for fourth level administrative division, varchar(20)
    population        : bigint (8 byte int)
    elevation         : in meters, integer
    dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
    timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
    modification date : date of last modification in yyyy-MM-dd format
    ```

    ### NOTES

    Following field names have been modified for convenience and clarity

    #### cities15000.txt
    ```
    - geonameid       > city_id
    - name            > city_name
    - asciiname       > city_asciiname
    - alternatenames  > city_alternatenames
    - country_code    > country_a2

"""

import os
import pandas


geonames_columns = [
    # from cities15000.txt (Geonames)
    "city_id",
    "city_name",
    "city_asciiname",
    "city_alternatenames",
    "latitude",
    "longitude",
    "feature_class",
    "feature_code",
    "country_a2",
    "cc2",
    "admin1",
    "admin2",
    "admin3",
    "admin4",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification_date",
]

regions_columns = [
    # from global_regions_v1.geojson
    "country_code",
    "country_name",
    "region_name",
    "subregion_name",
    "region_name_local",
    "bbox",
    "region_id",
]

to_drop = [
    "feature_class",
    "feature_code",
    "country_a2",
    "cc2",
    "admin1",
    "admin2",
    "admin3",
    "admin4",
    "elevation",
    "dem",
    "timezone",
    "modification_date",
]

# the directory of this file
root = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_global_locations_raw():
    filename = os.path.join(root, "temp/global_locations_v1_raw.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError("./temp/global_locations_v1_raw.csv not found.")

    locations_df = pandas.read_csv(filename, sep="\t")
    locations_df.columns = geonames_columns + regions_columns
    locations_df.sort_values(
        ["country_code", "city_name"], ascending=True, inplace=True
    )
    locations_df.drop(columns=to_drop, inplace=True)
    locations_df.set_index("city_id", inplace=True)
    return locations_df


def load_global_regions():
    # regions field to merge
    filename = os.path.join(root, "temp/global_regions_v1.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError("./temp/global_regions_v1.csv not found.")

    regions_df = pandas.read_csv(filename, sep="\t")
    regions_df.columns = regions_columns
    regions_df.sort_values("country_code", ascending=True, inplace=True)
    return regions_df


def load_city2region_lookup():
    # cities2regions lookup table
    filename = os.path.join(root, "oob_city2region_map.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError("oob_city2region_map.csv not found.")

    oob_lookup = pandas.read_csv(filename)
    return oob_lookup


def enrich_oob_lookup_with_regions(oob_lookup, regions_df):
    # enrich lookup table to merge all attributes at once
    matching_key = ["country_name", "region_name", "subregion_name"]
    manual_matched_regions = oob_lookup.merge(
        regions_df, left_on=matching_key, right_on=matching_key
    ).set_index("city_id")
    return manual_matched_regions


def update_unmatched(locations_df, manual_matched_regions):
    # replace empty rows with manually matched regions
    locations_df.loc[
        manual_matched_regions.index, regions_columns
    ] = manual_matched_regions
    return locations_df


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Build Global Regions basemap.")
    parser.add_argument(
        "--test", action="store_true", default=False, help="Enable tests."
    )
    args = parser.parse_args()

    # load inputs
    locations_df = load_global_locations_raw()
    regions_df = load_global_regions()
    oob_lookup = load_city2region_lookup()

    print(
        "{} unmatched features in global_locations_v1_raw.csv".format(
            locations_df.region_id.isna().sum()
        )
    )

    # merge regions_df and oob_lookup
    manual_matched_regions = enrich_oob_lookup_with_regions(oob_lookup, regions_df)

    # update unmatched rows with manually matched attributes
    updated_locations_df = update_unmatched(locations_df, manual_matched_regions)

    # unmatched are those cities outside their bbox (e.g. islands, costal cities, ...)
    print(
        "{} unmatched features after cleaning".format(
            updated_locations_df.region_id.isna().sum()
        )
    )

    if not args.test:
        # cache file
        output_filepath = os.path.join(root, "temp/global_locations_v1.tsv")
        updated_locations_df.to_csv(
            output_filepath, sep="\t", index_label="city_id", encoding="utf-8"
        )
        print("saved to", output_filepath)
