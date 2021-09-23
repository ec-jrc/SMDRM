# Sanitizer

Dockerized service to sanitize the text data of compressed JSON files coming from the `sanitize` RabbitMQ queue.

A common data model, defined in [event.py](../commons/src/libdrm/datamodel/event.py) is enforced for all valid events.
After the event text field is sanitized, this is sent to the `annotate` RabbitMQ queue, and it is ready to be received
by the next service in the pipeline: the [Annotator](../annotator/README.md).


## Build

```shell
make image
```

## Run

The Sanitizer service expects a running RabbitMQ service to send events to a queue.
For more info on how to run the RabbitMQ service, check the [Makefile](../commons/Makefile).

```shell
docker run --rm --name sanitizer sanitizer
```

## Tests

```shell
make unittests
```

## Credits
