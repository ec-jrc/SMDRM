import pytest
import zipfile

from libdrm import datamodels


def test_upload_has_valid_content(valid_zipfile):
    assert datamodels.upload.has_valid_content(valid_zipfile) is None


def test_upload_has_invalid_content(invalid_zipfile):
    with pytest.raises(zipfile.BadZipfile):
        datamodels.upload.has_valid_content(invalid_zipfile)


def test_upload_iter_content_with_valid_zipfile(valid_zipfile):
    for file in datamodels.upload.iter_content(valid_zipfile):
        assert isinstance(file, zipfile.ZipExtFile)
        assert file.name == "valid.json"


def test_upload_iter_content_with_invalid_zipfile(invalid_zipfile):
    with pytest.raises(zipfile.BadZipfile):
        for _ in datamodels.upload.iter_content(invalid_zipfile):
            pass


def test_schema_upload_with_valid_zip_file(valid_zipfile):
    """
    `zip_file` key is required and must match the
    variable name of marshmallow.fields.Raw()
    """
    schema = datamodels.upload.ZipFileUploadSchema()
    errors = schema.validate({"zip_file": valid_zipfile})
    assert not errors


def test_schema_upload_with_invalid_zip_file(invalid_zipfile):
    """
    `zip_file` key is required and must match the
    variable name of marshmallow.fields.Raw()
    """
    schema = datamodels.upload.ZipFileUploadSchema()
    errors = schema.validate({"zip_file": invalid_zipfile})
    assert errors == {"zip_file": ["Uploaded file is not a zip file."]}
