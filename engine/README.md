# Engine API

Dockerized service to start the data processing pipeline in the event of a successful file upload notification.

The file upload notification comes from the Upload API in the form of a JSON formatted _metadata_ payload.

> :information_source: For more info, see the _Table 1: Upload Metadata_ in the [Upload API](../upload/README.md).

The _metadata_ payload received from the Upload API contains your input. This includes the filename of the
uploaded zip file, and the annotator(s) you want to enrich data points with.

> :information_source: It is possible to enable multiple annotations (if available) using the metadata
> field [`<annotator_name>_annotator`](../upload/README.md#metadataupload).
> [api.py](api.py) `parse_extra_annotation_steps_from_meta()` function establishes the logic that enables
> to enrich batches of data points with multiple annotators.

## Instructions

> :information_source: The following commands are executed from the project root directory

### Build
```shell
docker-compose build engine
```

### Run
```shell
docker-compose up engine
```

During startup time, the Engine API will check on the status of all APIs it depends on included in the
[`libdrm.apis.APIs_lookup`](../build/libdrm/src/libdrm/apis.py) dictionary lookup.

> :information_source: You do not directly interact with the Engine API.
> You can do so only via the [Upload API](../upload/README.md).

### Tests

```shell
```
