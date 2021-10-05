import pathlib
import pytest
import zipfile
from unittest.mock import Mock
import libdrm.datamodels

from conftest import pipelines


def test_iter_zip_files(valid_zipfile, invalid_zipfile):
    # skip invalid zip file
    # _file should always be the valid zip file
    for _file in pipelines.iter_zip_files([valid_zipfile, invalid_zipfile]):
        assert isinstance(_file, pathlib.Path)
        assert _file == valid_zipfile


def test_iter_zip_file_content(valid_zipfile):
    for _file in pipelines.iter_zip_file_content([valid_zipfile]):
        assert isinstance(_file, zipfile.ZipExtFile)
        assert _file.name == "valid.json"


def test_iter_json_file_content(valid_zipfile, valid_json):
    json_files = pipelines.iter_zip_file_content([valid_zipfile])
    for _row in pipelines.iter_json_file_content(json_files):
        assert _row == valid_json


def test_iter_json_file_content_invalid(valid_zipfile_invalid_json):
    json_files = pipelines.iter_zip_file_content([valid_zipfile_invalid_json])
    for _row in pipelines.iter_json_file_content(json_files):
        assert _row == "this is not JSON!"


def test_iter_disaster_data_points(valid_json):
    for data_point in pipelines.iter_disaster_data_points([valid_json]):
        assert data_point["id"] == 1
        assert data_point["disaster_type"] in libdrm.datamodels.disaster.DISASTER_TYPES
        assert "uploaded_at" in data_point
        assert "text_sanitized" in data_point
        assert "annotations" in data_point


def test_iter_disaster_data_points_invalid():
    """
    When `disaster_type` is not passed in the data, the pipeline step
    search for the env `DISASTER_TYPE`.
    """
    with pytest.raises(KeyError):
        for _ in pipelines.iter_disaster_data_points([{"unknown": "data"}]):
            pass


def test_iter_disaster_data_points_wrong_disaster_type():
    """
    When an unknown `disaster_type` is passed in the data, the pipeline step
    search for the env `DISASTER_TYPE`.
    """
    with pytest.raises(KeyError):
        for _ in pipelines.iter_disaster_data_points([{"disaster_type": "unknown"}]):
            pass


def test_iter_batch_annotate_floods(valid_json, monkeypatch):
    """
    Mock call_annotation_api() return value.
    Given an input batch of 4 items and a batch size of 2.
    We expect 2 api calls and payload yielded.
    """
    mocked_response = Mock()
    input_batch = [valid_json] * 4
    expected_output = [{**d, **{"annotation": 1.0}} for d in input_batch]
    mocked_response.json.return_value = {"batch": expected_output}
    monkeypatch.setattr("conftest.pipelines.call_annotation_api", mocked_response)
    n_calls = 0
    expected = 2
    for _ in pipelines.iter_batch_annotate(input_batch, batch_size=2):
        n_calls += 1
    assert n_calls == expected
