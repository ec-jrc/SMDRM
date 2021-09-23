# -*- coding: utf-8 -*-

import json
import logging
import typing
import zipfile


logger = logging.getLogger(__name__)


def is_zip_file(f: str) -> bool:
    """
    Check if file is zip file,
    Source: https://docs.python.org/3/library/zipfile.html#zipfile.is_zipfile
    """

    return zipfile.is_zipfile(f)


def test_zip_file(f: str) -> typing.Optional[str]:
    """
    Read all the files in the archive and check their CRC’s and file headers.
       Return the name of the first bad file, or else return None.
    Source: https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.testzip
    """

    with zipfile.ZipFile(f, "r") as zf:
        return zf.testzip()


def safe_json_parser(data: bytes) -> dict:
    """
    Safely parse JSON data from bytes.
    Return empty dictionary if data is not valid JSON.
    """

    try:
        return json.loads(data)
    except ValueError as e:
        logger.warning(e)
        return {}


def iter_zip_content(_file: str) -> typing.Iterable[bytes]:
    """
    Extract zip file content file by file, line by line.
    """
    # TODO: implement batching

    with zipfile.ZipFile(_file, "r") as archive:
        for file in archive.infolist():
            with archive.open(file) as rows:
                for bytes_ in rows:
                    yield bytes_


def extract(file: str) -> typing.Iterable[dict]:
    """
    Extract function validates, and read JSON payload line from each file in zip file.
    """
    # zipfile validator
    if not is_zip_file(file):
        raise ValueError("not a zip file.")
    if test_zip_file(file) is not None:
        raise ValueError("invalid zip file.")
    # iter lines from files in the zip file
    for index, line in enumerate(iter_zip_content(file)):
        data = safe_json_parser(line)
        if not data:
            logger.warning("Event is not a valid JSON.")
            logger.debug(line)
            continue
        yield data
