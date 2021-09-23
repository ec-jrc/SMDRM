import dataclasses
import os


@dataclasses.dataclass()
class Config:
    timezone: str = os.getenv("TIMEZONE", "UTC")
