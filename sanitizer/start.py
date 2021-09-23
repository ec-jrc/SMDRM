# -*- coding: utf-8 -*-

from src.sanitizer import sanitize

from libdrm import (
    rabbitmq,
    datamodel,
)


def sanitizer_callback(body: bytes):
    # make event
    event = datamodel.DisasterEvent.from_bytes(body)
    # sanitize
    event.sanitize_text(sanitize)
    # sent to next queue
    print("event is sanitized")


if __name__ == "__main__":
    listening = True
    while listening:
        try:
            rabbitmq.consume(callback_logic=sanitizer_callback)
        except KeyboardInterrupt:
            listening = False
