#!/usr/bin/env python

from libdrm.rabbitmq import (
    config,
    client,
)

# test config
conf = config.TestConfig
# establish a connection with the RabbitMQ server
connection, channel = client.connect(conf)
# publish message
body = b"not the best message, but it will do"
client.publish(body, channel, conf)
print(" [x] Sent {}".format(body.decode()))
