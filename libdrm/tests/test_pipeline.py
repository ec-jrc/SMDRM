import pydantic
import pytest
import zipfile
import libdrm.pipeline


def test_init_DisasterModel_with_valid_json(valid_json):
    """Test __init__ method. id, created_at, lang, and text fields must be specified to use the default method."""
    m = libdrm.pipeline.DisasterModel(**valid_json)
    # assert required
    assert m.id == 123456789
    assert m.created_at == "Sat May 15 08:49:13 +0000 2021"
    assert m.lang == "it"
    assert m.text == "A text to be annotated with floods model"


def test_init_DisasterModel_with_invalid_json(invalid_json):
    """DisasterModel should raise a Pydantic error if not all required fields are set."""
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        libdrm.pipeline.DisasterModel(**invalid_json)


def test_init_DisasterModel_annotations_as_empty_list(valid_json):
    """DisasterModel annotations should be an empty list if not present in the data point."""
    m = libdrm.pipeline.DisasterModel(**valid_json)
    assert (
        m.annotations == []
    ), "If not present in data point, annotations should be an empty list"


def test_init_DisasterModel_annotations_as_defined_in_data_point(valid_json):
    """If present in the data point, DisasterModel annotations should be as the annotations field in the data point."""
    data_point = valid_json.copy()
    expected = {
        "annotations": [
            {
                "annotation_type": "floods",
                "annotation_prob": "1.0",
                "sanitized_text": "a text to be annotated with floods model",
            }
        ]
    }
    data_point.update(expected)
    m = libdrm.pipeline.DisasterModel(**data_point)
    assert (
        m.annotations == data_point["annotations"]
    ), "If present in the data point, annotations field should be as the annotations field in the data point."


def test_init_DisasterModel_optional_location_attributes(valid_json):
    """DisasterModel location attributes should be None if not present in the data point."""
    m = libdrm.pipeline.DisasterModel(**valid_json)
    for opt in ("latitude", "longitude", "place_name", "place_type"):
        # location attribute is present
        assert hasattr(m, opt)
        # location attribute is initialized as None
        assert m.dict()[opt] is None


def test_ZipFilesToJSONFiles_step_with_valid_zipfile(valid_zipfile):
    """Test ZipFilesToJSONFiles Pipeline Step logic with valid input."""
    step = libdrm.pipeline.ZipFilesToJSONFiles()
    json_file = next(step.logic([valid_zipfile]))
    assert isinstance(json_file, zipfile.ZipExtFile)
    assert json_file.name == "valid.json"


def test_ZipFilesToJSONFiles_step_with_invalid_zipfile(invalid_zipfile):
    """Test ZipFilesToJSONFiles Pipeline Step logic with invalid input."""
    step = libdrm.pipeline.ZipFilesToJSONFiles()
    with pytest.raises(zipfile.BadZipFile):
        next(step.logic([invalid_zipfile]))


def test_JSONFilesToJSONLines_step_with_valid_JSON_file_iterator_fixture(
    valid_json_files_iterator,
):
    """Test JSONFilesToJSONLines Pipeline Step logic with valid JSON files iterator fixture."""
    step = libdrm.pipeline.JSONFilesToJSONLines()
    json_bytes = next(step.logic(valid_json_files_iterator))
    assert json_bytes == {
        "id": "123456789",
        "created_at": "Sat May 15 08:49:13 +0000 2021",
        "text": "A text to be annotated with floods model",
        "lang": "it",
    }


def test_JSONFilesToJSONLines_step_with_invalid_JSON_file_iterator_fixture(
    invalid_json_files_iterator,
):
    """Test JSONFilesToJSONLines Pipeline Step logic with invalid JSON files iterator fixture.
    It raises StopIteration because the iterator is empty.
    The JSON validation try/except in JSONFilesToJSONLines
    catches the invalid bytes line in the JSON file (see conftest.py, line 80)
    TIP:
        run pytest with -s flag to see the dedicated WARNING in the Captured log call.
    """
    step = libdrm.pipeline.JSONFilesToJSONLines()
    with pytest.raises(StopIteration):
        next(step.logic(invalid_json_files_iterator))


def test_LegacyJSONLinesParser_step_with_valid_legacy_JSON_input(
    valid_json
):
    """Test JSONLinesToDataPoints Pipeline Step logic with valid JSON payload wrapped as legacy data."""
    step = libdrm.pipeline.LegacyJSONLinesParser()
    # legacy data is the raw data point wrapped in the `tweet` field
    legacy_data = iter([dict(tweet=valid_json)])
    raw_json = next(step.logic(legacy_data))
    assert raw_json == {
        "id": "123456789",
        "created_at": "Sat May 15 08:49:13 +0000 2021",
        "text": "A text to be annotated with floods model",
        "lang": "it",
    }


def test_LegacyJSONLinesParser_step_with_unknown_legacy_field_and_valid_JSON_input(
    valid_json
):
    """Test JSONLinesToDataPoints Pipeline Step logic with unknown legacy field (wrapping legacy JSON payload).
    It raises StopIteration because the iterator is empty.
    The legacy_data_model_field in LegacyJSONLinesParser is not found in the JSON dictionary so it yield it as is.
    The next step JSONLinesToDataPoints receives invalid data and skip it.
    TIP:
        run pytest with -v flag to see the dedicated WARNING in the Captured log call.
    """
    steps = [
        libdrm.pipeline.LegacyJSONLinesParser(),
        libdrm.pipeline.JSONLinesToDataPoints(),
    ]
    # legacy data is the raw data point wrapped in the `tweet` field
    legacy_data = iter([dict(invalid_legacy_field=valid_json)])
    pipeline = libdrm.pipeline.Pipeline(legacy_data, steps).build()
    with pytest.raises(StopIteration):
        next(pipeline)


def test_JSONLinesToDataPoints_step_with_valid_JSON_lines_iterator_fixture(
    valid_json_bytes_iterator,
):
    """Test JSONLinesToDataPoints Pipeline Step logic with valid JSON bytes iterator fixture."""
    step = libdrm.pipeline.JSONLinesToDataPoints()
    data_point = next(step.logic(valid_json_bytes_iterator))
    assert isinstance(data_point, libdrm.pipeline.DisasterModel)


def test_BatchesOfBytes_step_with_valid_JSON_bytes_batches_iterator_fixture(
    valid_json_bytes_iterator,
):
    """Test InBatches Pipeline Step logic with valid JSON bytes batches iterator fixture."""
    total = 25
    batch_size = 5
    step = libdrm.pipeline.InBatches(batch_size=batch_size)
    batches = step.logic(valid_json_bytes_iterator)
    # compute the number of batches
    n_batches = 0
    for batch in batches:
        assert len(batch) == batch_size
        n_batches += 1
    # 25 data points / 5 data point per batch = 5 batches
    assert n_batches == total / batch_size
