# LIBDRM Commons

Common helper modules shared by the pipeline services.

## RabbitMQ

[What is RabbitMQ?](https://www.youtube.com/watch?v=7rkeORD4jSw)

### Run

```shell

docker run -it --rm --name rabbitmq-1 --hostname rabbitmq-1 -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```

Go to the RabbitMQ [Management UI](http://localhost:15672). Typically, the UI is exposed on port 15672.

## Data model

Bla