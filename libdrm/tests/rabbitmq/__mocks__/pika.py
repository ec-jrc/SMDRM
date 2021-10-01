"""
Mock pika Connection and Channel functionality
"""


class Channel:
    def __init__(self): pass
    def exchange_declare(self): pass
    def queue_declare(self, queue, durable): pass
    def queue_bind(self, queue, exchange): pass
    def basic_qos(self, prefetch_count): pass
    def basic_consume(self, queue, on_message_callback): pass
    def start_consuming(self): pass
    def basic_publish(self): pass
    def basic_ack(self): pass


class Connection:
    def __init__(self): pass
    def channel(self): return Channel()
