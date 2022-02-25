# Global Locations V1

Global Locations dataset (global_locations_v1.tsv) is the final output
that is used in the `geocode_tweets` task to geolocalize a given set of datapoints.

This file is made of 2 external inputs:
1. the Global Regions GeoJSON basemap 
2. the [Geonames](http://www.geonames.org/) database

The attributes table of the Global Regions GeoJSON file are joined into the attributes
table of Geonames DB using the `Join attributes by location` spatial operation to create
the Global Locations dataset, our final output.

## Global Regions

The Global Regions GeoJSON is a [GADM36](https://gadm.org/data.html) based basemap.
We use a combination of [GADM levels](#GADM-Levels) from 0 to 2 with regards to the
region type and size.

We use the level 0 (Country level) to extract small Countries like archipelagos.
Whereas, we use levels 1 and 2 to extract big Countries with different administrative levels
of subdivision like Brazil, US, or China.

## Global Cities (Geonames DB)

The [Geonames DB](https://download.geonames.org/export/dump/) is an open-source
database of world cities.

We use the `latitude`, and `longitude` coordinates, as well as the `name`, and
`alternatenames` (other names for the same city) of cities with +15000 dwellings.

The coordinates of one or many cities are assigned to the datapoint that contains
Geo Political Entities (GPE) in text that match those of the cities.

## Instructions

> :bangbang:
> * execute all bash commands from project root directory
> * all directories here mentioned are relative to this file
> * we use [QGIS](https://www.qgis.org/en/site/) OpenSource GIS application to execute spatial operations
> * time consuming tasks are marked with :coffee: emoji

How to create the basemap from stratch, and the Global Location dataset.

Download the following external resources:
* [GADM36 shapefiles](https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_shp.zip)
* [Geonames cities15000.txt](https://download.geonames.org/export/dump/cities15000.zip)

> :coffee: This may take several minutes depending on you connection.

You can execute the Python scripts inside a Docker container

```shell
docker container run --rm -it -v $(pwd)/tools/places:/places -w /places python:3.8-slim bash
```

### Create Global Regions

Steps:
1. load levels 0, 1, and 2
2. for each level,
  select polygons using the proper [SQL statement](#SQL-Statements),
  and `Select Features by Expression...` QGIS algorithm
3. export/Save Selected Features As...
4. select GeoJSON from drop down menu
5. set WRITE_BBOX to YES in layer options
6. click OK

Add the *.geojson files in the ./temp/inputs directory.
Then, execute the following 

```shell
# add --test to inspect the output
python tools/places/build_global_regions.py
```

> :coffee: This may take few minutes depending on you hardware.

This outputs a single global_regions_v1.geojson file with the features selected in the steps above.

#### GADM Levels

* GID_0: Country ISO 3
* NAME_0: Country Name
* NAME_1: Region name
* NAME_2: (Sub)Region name
* NL_NAME_1: Region name in local language
* NL_NAME_2: (Sub)Region name in local language

* Level 0 areas
```example
{'GID_0': 'AIA', 'NAME_0': 'Anguilla'}
```

* Level 1 areas
```example
{'GID_0': 'CHL', 'NAME_0': 'Chile', 'GID_1': 'CHL.1_1', 'NAME_1': 'Aisén del General Carlos Ibáñez del Campo', 'VARNAME_1': 'Aisén|Aysén|Aysén del General Carlos Ibáñez del Campo', 'NL_NAME_1': None, 'TYPE_1': 'Región', 'ENGTYPE_1': 'Region', 'CC_1': 'XI', 'HASC_1': 'CL.AI'}
```

* Level 2 areas
```example
{'GID_0': 'AUS', 'NAME_0': 'Australia', 'GID_1': 'AUS.1_1', 'NAME_1': 'Ashmore and Cartier Islands', 'NL_NAME_1': None, 'GID_2': 'AUS.1.1_1', 'NAME_2': 'Ashmore and Cartier Islands', 'VARNAME_2': None, 'NL_NAME_2': None, 'TYPE_2': 'Territory', 'ENGTYPE_2': 'Territory', 'CC_2': None, 'HASC_2': None}
```

#### SQL Statements

SQL statements are in [sql.txt](sql.txt) file.

Copy/paste the section with regards to the level you want to select/extract features.

> Important Notes
>
> For unknown reasons, Bedfordshire in England (UK) is not selected using the SQL statement for level 2 (sub)regions.
> Thus, this should be manually extracted, and converted to geojson as described [above](#basemap).

### Create Global Cities

Steps:
* extract the text file from cities15000.zip
* load it as CSV file Layer/Add Layer/Add Delimited Text Layer
* activate the spatial index to enable spatial operations

Now, Global Regions from the previous step can be joined onto
this layer by means of the `Join attributes by location` spatial operation.

### Create Global Locations

Steps:
1. :coffee: load the [Global Regions GeoJSON](#create-global-regions) file
2. :coffee: (_optional_) transform it into a ESRI Shapefile makes next steps much faster
3. load the Global Cities CSV file
4. :coffee: run `Join attributes by location` spatial operation using 3. as base layer, and 1. as join layer,
   select `within`, and `touches` boxes for the appropriate topology rules,
   if you leave the default settings, a temporary layer will be created
5. extract the Joined layer attributes table as CSV,
   use tab separation and set no geometry,
   save it into ./temp/global_locations_v1_raw.csv
6. extract the Global Regions attributes table as CSV,
   use tab separation and set no geometry,
   save it into ./temp/global_regions_v1.csv.

Steps 5 and 6 create the input files to generate the final output, the Global Locations dataset.

Last step is to clean the Global Locations dataset

```shell
# requires pandas library
python tools/places/clean_global_places.py
```

The python script expects the ./temp/global_regions_v1.csv file to organize the fields
and merge any missing region attribute.

> Important Notes
>
> There is a solid chance that there are few cities whose coordinates fall outside
> the region bounding box they belong to. This produces cities with unmatched regions.
> This is not allowed for the region_id, as well as the city coordinates is a strict
> requirement of the `geocode_tweets` task

