# -*- coding: utf-8 -*-

import pika
import typing

from .config import DefaultConfig


def connect(conf: typing.Type[DefaultConfig]):
    # connection config
    params = pika.ConnectionParameters(host=conf.host)
    # establish a connection with the RabbitMQ server
    connection = pika.BlockingConnection(params)
    return connection, connection.channel()


def disconnect(connection, channel=None):
    # channel is passed to disconnect a consumer
    if channel is not None:
        channel.stop_consuming()
    connection.close()


def publish(body: bytes, channel, conf: typing.Type[DefaultConfig]):
    """
    Publish/send messages to a user defined queue via an exchange.
    Notes:
        Set `host=container_name` when running as a Docker stack in production.
    """
    channel.queue_declare(queue=conf.queue, durable=conf.durable)
    channel.exchange_declare(exchange=conf.exchange, exchange_type=conf.exchange_type)
    channel.queue_bind(queue=conf.queue, exchange=conf.exchange)
    channel.basic_publish(
        routing_key=conf.queue,
        exchange=conf.exchange,
        body=body,
        # make message persistent if RabbitMQ node restarts
        properties=pika.BasicProperties(delivery_mode=conf.delivery_mode),
    )


def subscribe(channel, callback: typing.Callable, conf: typing.Type[DefaultConfig]):
    """
    Subscribe to a user defined queue via an exchange.
    Then, handle consumed messages with a service specific callback.
    Notes:
        Set `host=container_name` when running as a Docker stack in production.
    """
    channel.queue_declare(queue=conf.queue, durable=conf.durable)
    channel.queue_bind(queue=conf.queue, exchange=conf.exchange)
    channel.basic_qos(prefetch_count=conf.prefetch_count)
    channel.basic_consume(queue=conf.queue, on_message_callback=callback)


def get_single_message(channel, conf: typing.Type[DefaultConfig]):
    """
    Get a single message from a user-defined queue.
    It is a great testing helper.
    """
    method_frame, header_frame, body = channel.basic_get(queue=conf.queue)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return method_frame, header_frame, body
    else:
        print("No message returned")
        return None
