class DefaultConfig:
    host: str = None
    exchange: str = None
    exchange_type: str = "direct"
    queue: str = None
    # queue will survive a RabbitMQ node restart
    durable: bool = True
    # basic.qos protocol method tells RabbitMQ not to give more than one message to a worker at a time.
    # In other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
    # Instead, it will dispatch it to the next worker that is not still busy.
    prefetch_count: int = 1
    # make message persistent if RabbitMQ node restarts
    delivery_mode: int = 2


class TestConfig(DefaultConfig):
    host: str = "localhost"
    exchange: str = "test-exchange"
    queue: str = "test-queue"
