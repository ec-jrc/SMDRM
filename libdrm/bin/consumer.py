#!/usr/bin/env python

import os
import sys

from libdrm.rabbitmq import (
    config,
    client,
)


def _callback(channel, method, properties, body):
    """
    In order to make sure a message is never lost, RabbitMQ supports message acknowledgments.
    An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message had been
    received, processed and that RabbitMQ is free to delete it.
    If a consumer dies (its channel is closed, connection is closed, or TCP connection is lost) without sending
    an ack, RabbitMQ will understand that a message wasn't processed fully and will re-queue it. If there are
    other consumers online at the same time, it will then quickly redeliver it to another consumer. That way you
    can be sure that no message is lost, even if the workers occasionally die.
    There aren't any message timeouts; RabbitMQ will redeliver the message when the consumer dies. It's fine even
    if processing a message takes a very, very long time.
    Source: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
    """
    print(" [x] Received {}".format(body.decode()))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Acknowledged")


# test config
conf = config.TestConfig
# establish a connection with the RabbitMQ server
connection, channel = client.connect(conf)
# consumer
client.subscribe(channel, _callback, conf)

try:
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
