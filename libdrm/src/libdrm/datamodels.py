import json
import pydantic
import typing
import zipfile


class DataPointModel(pydantic.BaseModel, extra=pydantic.Extra.ignore):
    """A Pydantic validator class that ignores unknown fields,
    and fails on missing fields of a given datapoint."""

    id: int
    created_at: str
    lang: str
    text: str
    # enriched fields
    # generated at runtime by pipeline tasks
    # tranform placeholder
    text_clean: typing.Optional[str] = None
    # geocode placeholder
    place: typing.Optional[dict] = None
    # annotators placeholder
    annotation: typing.Optional[dict] = None


class ZipFileModel:
    """A class representation to handle input zip files"""

    def __init__(self, path: str):
        self.path = path

    def is_valid(self) -> bool:
        """Return False is path is not a zip file or it does not exist."""
        return zipfile.is_zipfile(self.path)

    def iter_bytes(self) -> typing.Iterable[bytes]:
        """Iterate content of extracted files from a zip file,
        one line at the time."""
        with zipfile.ZipFile(self.path, "r") as archive:
            for zip_ext_file in archive.infolist():
                with archive.open(zip_ext_file) as content:
                    yield from content

    def iter_jsonl(self) -> typing.Iterable[dict]:
        """Iterate content of extracted files from a zip file,
        one line at the time but converted to JSON."""
        for json_bytes in self.iter_bytes():
            try:
                yield json.loads(json_bytes)
            except json.decoder.JSONDecodeError:
                # empty dict at failure
                yield None

    def cache(self, output_path: str, jsonl_batch_gen: typing.Iterable[str]) -> None:
        """Cache processed NDJSON batches to zip file and collect metrics."""
        with zipfile.ZipFile(output_path, "w") as zf:
            for batch_id, batch_jsonl in enumerate(jsonl_batch_gen, start=1):
                # write ndjson batch to zip file
                zf.writestr("{}.ndjson".format(batch_id), batch_jsonl)

