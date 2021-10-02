# -*- coding: utf-8 -*-

from __future__ import annotations
import dataclasses
import typing
import zipfile
import werkzeug


@dataclasses.dataclass()
class ZipFileModel:
    """
    FileUploadModel Class creates instances of user-uploaded files and simplify common file operations.
    """

    # default uploaded file properties
    _file: typing.Type[werkzeug.datastructures.FileStorage]

    def is_valid_file(self) -> bool:
        """
        Check if file is zip file,
        Source: https://docs.python.org/3/library/zipfile.html#zipfile.is_zipfile
        """
        result = zipfile.is_zipfile(self._file)
        return result

    def has_valid_content(self) -> typing.Union[None, str]:
        """
        Read all the files in the archive and check their CRC’s and file headers.
        Return the name of the first bad file, or else return None.
        Source: https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.testzip
        """

        with zipfile.ZipFile(self._file, "r") as zf:
            return zf.testzip()

    def iter_content(self) -> typing.Iterable[bytes]:
        """
        Iter files out of the zip archive.

        """

        with zipfile.ZipFile(self._file, "r") as archive:
            for file in archive.infolist():
                with archive.open(file) as json_file:
                    yield json_file
