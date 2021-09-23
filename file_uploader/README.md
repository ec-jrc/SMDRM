# File Uploader

Dockerized service to upload compressed JSON files into the SMDRM pipeline.
The [Observer](https://refactoring.guru/design-patterns/observer/python/example) Design Pattern is used to build
a custom object that observes a user-defined path for new incoming file to be processed.

Uploaded files must be *.zip. The files in the archive must be formatted as follows:
* a JSON-formatted payload, aka DisasterEvent, one for each new line
* not larger than 1gb
* add another condition?

> :warning: **WARNING** :warning:
> events with invalid JSON format are discarded.

A common data model, defined in [event.py](../commons/src/libdrm/datamodel/event.py) is enforced for all valid events.
After the event data model is set, this is sent to the `sanitize` RabbitMQ queue, and it is ready to be received by
the next service in the pipeline: the [Sanitizer](../sanitizer/README.md).


## Build

```shell
make image
```

## Run

The Uploader service expects a running RabbitMQ service to send events to a queue.
For more info on how to run the RabbitMQ service, check the [Makefile](../commons/Makefile).

```shell
docker run --rm --name file_uploader -v ${PWD}/files_to_upload:/tmp/observed file_uploader
```

Now, add files.zip in the mapped path ./files_to_upload.

> :bulb: TIPS :bulb:
> cp <path/file.zip> ${PWD}/files_to_upload would to it.


## Tests

```shell
make unittests
```

## Credits
