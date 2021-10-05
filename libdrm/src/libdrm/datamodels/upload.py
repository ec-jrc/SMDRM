from __future__ import annotations
import marshmallow.validate
import typing
import zipfile


def has_valid_content(path) -> typing.Union[None, str]:
    """
    Read all the files in the archive and check their CRC’s and file headers.
    Return the name of the first bad file, or else return None.
    Source: https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.testzip
    """

    with zipfile.ZipFile(path, "r") as zf:
        return zf.testzip()


def iter_content(path: str) -> typing.Iterable[zipfile.ZipExtFile]:
    """
    Iter extracted files out of the zip archive.
    """

    with zipfile.ZipFile(path, "r") as archive:
        for file in archive.infolist():
            with archive.open(file) as ext_file:
                yield ext_file


def validate_zip_file(path):
    if not zipfile.is_zipfile(path):
        raise marshmallow.ValidationError("Uploaded file is not a zip file.")
    if has_valid_content(path) is not None:
        raise marshmallow.ValidationError("Invalid zip file content uploaded.")


class ZipFileUploadSchema(marshmallow.Schema):
    zip_file = marshmallow.fields.Raw(
        type="file",
        required=True,
        validate=validate_zip_file,
    )
