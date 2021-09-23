# -*- coding: utf-8 -*-

import pathlib
import pytest
import sys

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from src.extractor import extract


def test_extract():
    expected = 5
    extracted = 0
    for _ in extract(root/"tests/test_data.zip"):
        # last line fails because of bad synthesized JSON data
        extracted += 1
    assert expected == extracted


def test_bad_zipfile():
    tmp_bad_zipfile = root/"tests/tmp_data.zip"
    with open(tmp_bad_zipfile, "w") as zipfile:
        zipfile.write("invalid zip file data. just testing")

    with pytest.raises(ValueError):
        for _ in extract(tmp_bad_zipfile):
            continue
    # remove tmp file
    tmp_bad_zipfile.unlink()
