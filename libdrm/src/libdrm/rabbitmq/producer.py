#!/usr/bin/env python

import pika

from .config import Config


def produce(message: bytes):
    """
    RabbitMQ Producer produces messages into a user defined queue.
    Defined with RABBITMQ_QUEUE environment variable.
    Notes:
        Set `RABBITMQ_HOST=container_name` when running services in Docker.
    """
    # establish a connection with the RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.host)
    )
    channel = connection.channel()

    # The next step, just like before, is to make sure that the queue exists. Creating a queue using queue
    # declare is idempotent ‒ we can run the command as many times as we like, and only one will be created.
    # durable=True makes sure the queue will survive a RabbitMQ node restart
    channel.queue_declare(queue=Config.queue, durable=True)

    # In RabbitMQ a message can never be sent directly to the queue,
    # it always needs to go through an exchange.
    # A default exchange identified by an empty string is special:
    # it allows us to specify exactly to which queue the message should go.
    # The queue name needs to be specified in the routing_key parameter
    channel.basic_publish(
        exchange='',
        routing_key=Config.queue,
        body=message,
        properties=pika.BasicProperties(
            # make message persistent if RabbitMQ node restarts
            delivery_mode=2,
        ))

    print(" [x] Sent {}".format(message))

    # Before exiting the program we need to make sure the network buffers were flushed and our
    # message was actually delivered to RabbitMQ. We can do it by gently closing the connection.
    connection.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Publish (or send) messages to a RabbitMQ queue."
    )

    # the message, task, event, or whatever you wanna call it
    messages = ["#1 msg ...", "#2 msg ...", "#3 msg ...", "#4 msg ..."]

    for msg in messages:
        # send bytes message to RabbitMQ queue on host
        produce(msg.encode("utf-8"))
