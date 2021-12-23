import typing as t


class Pipeline:
    """Pipeline Class represents a data pipeline made by a concatenation of steps.
    Each step is generator that applies a specific transformation to the stream of data."""

    def __init__(self, steps: t.List[t.Tuple[t.Callable, t.Optional[dict]]] = None):
        self.steps = steps or list()

    def add(self, step: t.Iterable, kwargs: dict = None) -> None:
        self.steps.append((step, kwargs))

    def execute(self, datapoints: t.Iterable[bytes]) -> t.Iterable:
        print("Executing pipeline...")
        iterator = datapoints
        for step, kwargs in self.steps:
            iterator = step(iterator, **kwargs) if kwargs else step(iterator)
        return iterator