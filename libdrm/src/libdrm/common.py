import functools
import time
import typing as t


def iter_in_batches(generator: t.Iterable, batch_size: int = 1000) -> t.Iterable[list]:
    """Iterate a given generator in batches.
    Indicated for resources expensive tasks such as Annotations, and Geocoding."""
    batch = []
    for line in generator:
        batch.append(line)
        if len(batch) == batch_size:
            yield batch
            # flush batch
            batch.clear()
        continue
    # ensure all data points are yielded
    if batch:
        yield batch


def log_execution(logger):
    """
    Parent function to catch the __name__ argument passed as name.
    Log elapsed time for successful execution or Exception for failure.
    :return
    """

    def log(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # track elapsed time
                time_start = time.time()
                result = f(*args, **kwargs)
                elapsed = time.time() - time_start
                logger.info(f'{f.__name__}() completed in {elapsed:.4f}s')
                return result
            except Exception as e:
                logger.exception(f'Exception in {f.__name__}(): {str(e)}')

        return wrapper

    return log
