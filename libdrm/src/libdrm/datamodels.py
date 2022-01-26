import json
import pydantic
import typing as t
import zipfile


class DataPointModel(pydantic.BaseModel, extra=pydantic.Extra.ignore):
    """A Pydantic validator class that ignores unknown fields,
    and fails on missing fields of a given data point."""

    id: int
    created_at: str
    lang: str
    text: str
    # enriched fields
    # optional because generated at runtime @ transform_tweets
    text_clean: t.Optional[str] = None
    places: t.Optional[list] = None


class ZipFileModel:
    """A class representation to handle input zip files"""

    def __init__(self, path: str):
        self.path = path

    def is_valid(self) -> bool:
        """Return False is path is not a zip file or it does not exist."""
        return zipfile.is_zipfile(self.path)

    def iter_bytes(self) -> t.Iterable[bytes]:
        """Iterate content of extracted files from a zip file,
        one line at the time."""
        with zipfile.ZipFile(self.path, "r") as archive:
            for zip_ext_file in archive.infolist():
                with archive.open(zip_ext_file) as content:
                    yield from content

    def iter_jsonl(self) -> t.Iterable[dict]:
        """Iterate content of extracted files from a zip file,
        one line at the time but converted to JSON."""
        for json_bytes in self.iter_bytes():
            try:
                yield json.loads(json_bytes)
            except json.decoder.JSONDecodeError:
                # empty dict at failure
                yield dict()

    def cache(self, output_path: str, jsonl_batch_gen: t.Iterable[str]) -> None:
        """Cache processed NDJSON batches to zip file."""
        with zipfile.ZipFile(output_path, "w") as zf:
            for batch_id, batch_jsonl in enumerate(jsonl_batch_gen, start=1):
                # write ndjson batch to zip file
                zf.writestr("{}.ndjson".format(batch_id), batch_jsonl)

