import pytest
import zipfile
import libdrm.schemas


def test_MetadataUploadSchema_with_valid_metadata(valid_metadata):
    """Test MetadataUploadSchema Marshmallow Schema."""
    schema = libdrm.schemas.MetadataUploadSchema()
    errors = schema.validate(valid_metadata)
    assert not errors


def test_MetadataUploadSchema_with_invalid_metadata(invalid_metadata):
    """Test MetadataUploadSchema Marshmallow Schema."""
    schema = libdrm.schemas.MetadataUploadSchema()
    with pytest.raises(libdrm.schemas.marshmallow.ValidationError):
        schema.load(invalid_metadata)


def test_has_valid_content_with_valid_zipfile(valid_zipfile):
    """Test if uploaded zip file with valid content passes validation."""
    assert libdrm.schemas.has_valid_content(valid_zipfile) is None


def test_has_valid_content_with_invalid_zipfile(invalid_zipfile):
    """Test if uploaded zip file with invalid content throws a raise."""
    with pytest.raises(zipfile.BadZipfile):
        libdrm.schemas.has_valid_content(invalid_zipfile)


def test_ZipFileUploadSchema_with_valid_zip_file(valid_zipfile):
    """
    Test ZipFileUploadSchema Marshmallow Schema.
    `zip_file` key is required and must match the
    variable name of marshmallow.fields.Raw()
    """
    schema = libdrm.schemas.ZipFileUploadSchema()
    errors = schema.validate({"zip_file": valid_zipfile})
    assert not errors


def test_ZipFileUploadSchema_with_invalid_zip_file(invalid_zipfile):
    """
    Test ZipFileUploadSchema Marshmallow Schema.
    `zip_file` key is required and must match the
    variable name of marshmallow.fields.Raw()
    """
    schema = libdrm.schemas.ZipFileUploadSchema()
    errors = schema.validate({"zip_file": invalid_zipfile})
    assert errors == {"zip_file": ["Uploaded file is not a zip file."]}
