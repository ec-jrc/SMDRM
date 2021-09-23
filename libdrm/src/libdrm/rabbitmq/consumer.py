#!/usr/bin/env python

import os
import pika
import sys
import typing

from .config import Config


def consume(callback_logic: typing.Callable):
    """
    RabbitMQ Consumer consumes messages from a user defined queue.
    Defined with RABBITMQ_QUEUE environment variable.
    Notes:
        Set `RABBITMQ_HOST=container_name` when running services in Docker.
    """
    # establish a connection with the RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.host))
    channel = connection.channel()

    # You may ask why we declare the queue again ‒ we have already declared it in our previous code.
    # We could avoid that if we were sure that the queue already exists. For example if send.py program was run before.
    # But we're not yet sure which program to run first. In such cases it's a good practice to repeat declaring the
    # queue in both programs.
    channel.queue_declare(queue=Config.queue, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received {}".format(body.decode()))
        callback_logic(body)
        # Doing a task can take a few seconds. You may wonder what happens if one of the consumers starts a long task
        # and dies with it only partly done. With our current code once RabbitMQ delivers message to the consumer it
        # immediately marks it for deletion. In this case, if you kill a worker we will lose the message it was just
        # processing. We'll also lose all the messages that were dispatched to this particular worker but were not
        # yet handled.
        # But we don't want to lose any tasks. If a worker dies, we'd like the task to be delivered to another worker.
        # In order to make sure a message is never lost, RabbitMQ supports message acknowledgments.
        # An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message had been
        # received, processed and that RabbitMQ is free to delete it.
        # If a consumer dies (its channel is closed, connection is closed, or TCP connection is lost) without sending
        # an ack, RabbitMQ will understand that a message wasn't processed fully and will re-queue it. If there are
        # other consumers online at the same time, it will then quickly redeliver it to another consumer. That way you
        # can be sure that no message is lost, even if the workers occasionally die.
        # There aren't any message timeouts; RabbitMQ will redeliver the message when the consumer dies. It's fine even
        # if processing a message takes a very, very long time.
        # Source: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Acknowledged")

    # basic.qos protocol method tells RabbitMQ not to give more than one message to a worker at a time.
    # In other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
    # Instead, it will dispatch it to the next worker that is not still busy.
    channel.basic_qos(prefetch_count=1)
    # tell RabbitMQ that the callback function should receive messages from our defined queue
    channel.basic_consume(queue=Config.queue, on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    import argparse
    import time
    parser = argparse.ArgumentParser(
        description="Consume (or receive) messages from a RabbitMQ queue."
    )

    def test_callback(body: bytes):
        time.sleep(body.count(b'.'))

    try:
        consume(test_callback)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
