"""This module contains the Marshmallow Schemas to validate the User uploaded content.
The following schemas are available:
    * ZipFileUploadSchema: verify the validity of the uploaded zip file and its content
    * MetadataUploadSchema: verify the validity of the metadata input for customization of the annotations
"""

import marshmallow.validate
import zipfile


class MetadataUploadSchema(marshmallow.Schema):
    """Data Schema for user based uploaded metadata.
    Format: <disaster_type>_annotator
    """
    floods_annotator = marshmallow.fields.Boolean(load_default=False)
    fires_annotator = marshmallow.fields.Boolean(load_default=False)

    class Meta:
        unknown = marshmallow.EXCLUDE


def has_valid_content(path: str):
    """
    Read all the files in the archive and check their CRC’s and file headers.
    Return the name of the first bad file, or else return None.
    Source: https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.testzip
    """

    with zipfile.ZipFile(path, "r") as zf:
        return zf.testzip()


def validate_zip_file(path: str) -> None:
    """Schema helper function to validate uploaded zip file."""
    if not zipfile.is_zipfile(path):
        raise marshmallow.ValidationError("Uploaded file is not a zip file.")
    if has_valid_content(path) is not None:
        raise marshmallow.ValidationError("Invalid zip file content uploaded.")


class ZipFileUploadSchema(marshmallow.Schema):
    """Data Schema for uploaded zip file."""
    zip_file = marshmallow.fields.Raw(
        type="file",
        required=True,
        validate=validate_zip_file,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE
