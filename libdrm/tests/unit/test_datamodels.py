import pytest
import pydantic
from zipfile import BadZipFile

from libdrm.datamodels import DataPointModel, ZipFileModel


def test_DataPointModel_with_valid_input():
    """Test if DataPointModel.parse_raw validation is successful."""
    result = DataPointModel.parse_raw(
        b'{"id": "1", "created_at": "date", "lang": "id", "text": "text"}'
    )
    assert (
        str(result)
        == "id=1 created_at='date' lang='id' text='text' text_clean=None place=None annotation=None"
    )


def test_DataPointModel_with_invalid_input():
    """Test if DataPointModel validation fails due to invalid input format."""
    with pytest.raises(pydantic.ValidationError):
        DataPointModel.parse_raw(b"Does it look valid JSON bytes to you??")


def test_DataPointModel_with_enriched_input():
    """Test if DataPointModel validation is successful when the enriched input is given."""
    datapoint = DataPointModel.parse_raw(
        b'{"id": "1", "created_at": "date", "lang": "id", "text": "text", "text_clean": null, "place": null, "annotation": null}'
    )
    assert (
        datapoint.dict()
        == dict(datapoint)
        == {
            "id": 1,
            "created_at": "date",
            "lang": "id",
            "text": "text",
            "text_clean": None,
            "place": None,
            "annotation": None,
        }
    )


def test_is_zip_file_with_valid_zipfile(valid_archive_path):
    """Test if zip file at the given path is valid."""
    assert ZipFileModel(valid_archive_path).is_valid()


def test_is_zip_file_with_invalid_zipfile(invalid_archive_path):
    """Test if invalid zip file at the given path is invalid."""
    assert not ZipFileModel(invalid_archive_path).is_valid()


def test_iter_bytes_on_valid_zipfile(valid_archive_path):
    """Test if result of iter_jsonl_lines is bytes,
    and contains the specific ID on a valid zip file."""
    data = next(ZipFileModel(valid_archive_path).iter_bytes())
    assert isinstance(data, bytes)
    assert b"1405197058210992131" in data


def test_iter_bytes_on_invalid_zipfile(invalid_archive_path):
    """Test if result of iter_jsonl_lines raises BadZipFile on an invalid zip file."""
    with pytest.raises(BadZipFile):
        next(ZipFileModel(invalid_archive_path).iter_bytes())


def test_iter_json_on_valid_zipfile(valid_archive_path):
    """Test if result of iter_jsonl_lines is bytes,
    and contains the specific ID on a valid zip file."""
    data = next(ZipFileModel(valid_archive_path).iter_jsonl())
    assert isinstance(data, dict)
    assert data["tweet"]["id"] == 1405197058210992131


def test_iter_json_on_invalid_zipfile(invalid_archive_path):
    """Test if result of iter_jsonl_lines is bytes,
    and contains the specific ID on a valid zip file."""
    with pytest.raises(BadZipFile):
        next(ZipFileModel(invalid_archive_path).iter_jsonl())


def test_iter_json_on_valid_zipfile_wrong_data(wrong_archive_path):
    """Test model ignore invalid JSON data."""
    zf = ZipFileModel(wrong_archive_path)
    assert zf.is_valid()
    with pytest.raises(StopIteration):
        next(zf.iter_jsonl())
