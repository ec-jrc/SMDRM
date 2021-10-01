# -*- coding: utf-8 -*-

import pytest
from libdrm.rabbitmq import (
    client,
    config,
)

from unittest.mock import Mock
from .__mocks__ import pika


def test_connect(monkeypatch):
    """
    Test if pika's BlockingConnection Class is called when executing client.connect()
    """
    conf = config.TestConfig

    mocked_pika = Mock()
    mocked_pika.ConnectionParameters.return_value = "localhost"
    mocked_pika.BlockingConnection.return_value = pika.Connection()
    monkeypatch.setattr("libdrm.rabbitmq.client.pika", mocked_pika)

    client.connect(conf)

    mocked_pika.BlockingConnection.assert_called_once_with("localhost")


def test_client_connected_and_disconnect():
    conf = config.TestConfig
    # establish a connection with RabbitMQ server
    connection, channel = client.connect(conf)
    assert connection.is_open and channel.is_open
    client.disconnect(connection, channel=channel)
    assert not (connection.is_open and channel.is_open)


def test_client_produce_and_consume_one():
    conf = config.TestConfig
    # establish a connection with RabbitMQ server
    connection, channel = client.connect(conf)
    # publish a message
    input_body = b"not the best message, but it will do"
    client.publish(input_body, channel, conf)

    # consume the message
    method_frame, header_frame, output_body = client.get_single_message(channel, conf)
    assert input_body == output_body
    # no message in queue due to acknowledgment
    # assert method_frame.message_count == 0
    assert method_frame.exchange == "test-exchange"
    client.disconnect(connection, channel)
