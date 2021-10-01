# -*- coding: utf-8 -*-

import pathlib
import pytest

from libdrm.datamodels.file import FileUploadModel


root = pathlib.Path(__file__).resolve().parent.parent


def test_extract():
    """
    Test if extract() skip last row of zip file content due to invalid JSON.
    """
    expected = 5
    extracted = 0
    file_model = FileUploadModel(root/"test_data.zip")
    for _ in file_model.extract():
        # last line fails because of bad synthesized JSON data
        extracted += 1
    assert expected == extracted


def test_bad_zipfile():
    """
    Test a bad zip file created on the fly.
    """
    tmp_bad_zipfile = root/"tmp_data.zip"
    with open(tmp_bad_zipfile, "w") as zipfile:
        zipfile.write("invalid zip file data. just testing")

    file_model = FileUploadModel(tmp_bad_zipfile)
    with pytest.raises(ValueError):
        for _ in file_model.extract(tmp_bad_zipfile):
            continue
    # remove tmp file
    tmp_bad_zipfile.unlink()
