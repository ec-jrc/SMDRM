import os


class Config:
    queue: str = os.getenv("RABBITMQ_QUEUE", "dev-queue")
    host: str = os.getenv("RABBITMQ_HOST", "localhost")
