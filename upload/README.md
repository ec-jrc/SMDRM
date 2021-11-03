# Upload API

Dockerized service to upload compressed JSON files in the SMDRM service.
Uploads must pass a number of data sanitation steps before they are ready to be uploaded.

> :warning: Invalid zip files won't be uploaded, and lines in each of the JSON files in the zip file with
> invalid JSON format will be skipped.

## ZipFileUpload

A valid candidate for upload must:
* be a valid zip file
* contain valid JSON files i.e., a valid JSON-formatted dictionary, one for each new line

> :information_source: For more info, check the ZipFileUpload Marshmallow schema, and the `validate_zip_file()`
> function in [`libdrm.schemas.ZipFileUploadSchema`](../libdrm/src/libdrm/schemas.py).

For each uploaded zip file that passes the sanitation:
* a reference will be cached inside the `uploads` Docker Volume to be used by the Engine API Docker service
* an HTTP POST request with the upload _metadata_ will be sent to the Engine API as notification of successful upload.

### MetadataUpload

Upload metadata is an extension of the Upload API POST request form.
Table 1 shows how you can utilize the metadata to enable different annotations in the data processing pipeline.

|Field|Format|Effect|Examples|
|-----|------|------|--------|
|`filename`|str|The [(secure_)filename](https://tedboy.github.io/flask/generated/werkzeug.secure_filename.html) of the uploaded zip file|By default, the `filename` field with the name of the uploaded zip file is automatically added to each data point. Thus, you do NOT need to include it in the POST request form.|
|`<annotator_name>_annotator`|bool|Enables the annotation type to be executed|Annotate data points with Floods API: `--form "floods_annotator=1"`.<br>It accepts any [truthy](https://github.com/marshmallow-code/marshmallow/blob/e06e9ca3aac1b7389eda488b0627340c5cb3782d/src/marshmallow/fields.py#L1042-L1091) value.|

_Table 1. Upload Metadata_

> :information_source: For more info, check the MetadataUpload Marshmallow schema in
> [`libdrm.schemas.MetadataUploadSchema`](../libdrm/src/libdrm/schemas.py).

## Instructions

> :information_source: The following commands are executed from the project root directory

### Build
```shell
docker-compose build upload
```

### Run
```shell
docker-compose up upload
```

When the Upload and the Engine APIs are up and running, you can upload your zip file from you host machine as follows:

```shell
# replace /path/to/file.zip with the full path to the zip file on your host machine you want to upload
curl --form "floods_annotator=1" --form "zip_file=@/path/to/file.zip" "http://localhost:5000"
```

This example would upload `/path/to/file.zip` zip file to the `uploads` Docker Volume (see [docker-compose.yml](../docker-compose.yml)),
and it enables floods related annotations on the data points using the [Floods API](../annotators/floods/README.md).

> :information_source: `floods_annotator` value can take any of these
> [values](https://github.com/marshmallow-code/marshmallow/blob/e06e9ca3aac1b7389eda488b0627340c5cb3782d/src/marshmallow/fields.py#L1042-L1091).

### Tests

Initialize the test instance of the Upload API
```shell
docker-compose -f ./docker-compose.test.yml up --build upload
```

Run the tests with the dedicated [tester](tests/Dockerfile) Docker image
```shell
docker-compose -f ./docker-compose.test.yml up --build tester
```

Clean up tests
```shell
docker-compose -f ./docker-compose.test.yml down -v
```
