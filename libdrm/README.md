# LIBDRM

Common helper modules shared by the pipeline services.

LIBDRM contains SMDRM project specific modules, namely:
* datamodel
* rabbitmq


## Datamodel

The SMDRM service is intended for scientists and researchers to bring raw data, and obtain an enriched product.
Disaster type probability annotation and geo localization of events 
that can be analysed and reported back to their customers.


Although, data can take different forms, there is a set of required fields with which we create a data model.
A single data point, aka a disaster-related event, must have:
* `created_at`: the date and time of occurrence of the event
* `text`: the textual information for annotation
* `lang`: (optional) the language of the text field

The `DisasterEvent` Python class in `libdrm.datamodel` module structures events by enforcing a specific data model.
Import the class in any microservice to ensure the data consistency and to enable useful class methods
to interact with an event.


## RabbitMQ

[RabbitMQ](https://www.rabbitmq.com/) is an open source message broker.
SMDRM Docker microservices depends on its message queuing features to stream events from one another.

The `libdrm.rabbitmq` module features a common [producer](src/libdrm/rabbitmq/producer.py), and
a [consumer](src/libdrm/rabbitmq/consumer.py) functions that can be imported into any Docker service.
This allows any microservice to produce and/or consume events from a specific queue.

### Requirements

The [pika](https://pika.readthedocs.io/en/stable/) Python library is a pure-Python implementation of the AMQP 0-9-1
protocol, the same used by RabbitMQ.

### Config

There are 2 environment variables, namely `RABBITMQ_QUEUE` and `RABBITMQ_HOST` that need to be set accordingly for
each microservice.

### Run

The best way to run RabbitMQ is with Docker:

```shell
docker run -it --rm --name rabbitmq-1 --hostname rabbitmq-1 -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```

> :info: INFO :info:
> the `3.9-management` version comes with some management plugins pre-installed and it exposes a handy UI.
> Go to the RabbitMQ [Management UI](http://localhost:15672). Typically, the UI is exposed on port 15672.
