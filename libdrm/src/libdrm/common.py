import os
import functools
import time
import typing


def get_version(path: str):
    """Get version from a given text file.
    File content should be a single line with the version number e.g. 1.0.0"""
    with open(path_arg(path)) as v:
        return v.read()


def path_arg(path: str) -> str:
    """Custom path argument parser."""
    if not os.path.exists(path):
        raise FileNotFoundError("Path not found.")
    if os.path.isdir(path):
        raise ValueError("Path is a directory, but a zip file is expected.")
    return os.path.abspath(path)


def iter_in_batches(generator: typing.Iterable, batch_size: int = 1000) -> typing.Iterable[list]:
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
    """Log elapsed time for successful execution, or Exception for failure for a decodated function."""
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
