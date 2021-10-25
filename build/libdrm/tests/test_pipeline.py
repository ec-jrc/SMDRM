import pydantic
import pytest
import zipfile
import libdrm.pipeline


def test_init_DisasterModel_with_valid_json(valid_json):
    """
    Test class __init__ method. All fields must be specified to use the default method.
    """
    m = libdrm.pipeline.DisasterModel(**valid_json)
    # assert required
    assert m.id == 123456789
    assert m.created_at == 'Sat May 15 08:49:13 +0000 2021'
    assert m.lang == "it"
    assert m.text == "A text to be annotated with floods model"
    # assert optional
    for opt in ("latitude", "longitude", "place_name", "place_type", "uploaded_at"):
        assert hasattr(m, opt)


def test_init_DisasterModel_with_invalid_json(invalid_json):
    """
    DisasterModel should not be initialized with __init__ method
    if not all required fields are set
    """
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        libdrm.pipeline.DisasterModel(**invalid_json)


def test_ExtractJSONFilesFromZipFiles_step_with_valid_zipfile(valid_zipfile):
    """Test ZipFilesToJSONFiles Pipeline Step logic with valid input."""
    step = libdrm.pipeline.ZipFilesToJSONFiles()
    json_file = next(step.logic([valid_zipfile]))
    assert isinstance(json_file, zipfile.ZipExtFile)
    assert json_file.name == "valid.json"


def test_ExtractJSONFilesFromZipFiles_step_with_invalid_zipfile(invalid_zipfile):
    """Test ZipFilesToJSONFiles Pipeline Step logic with invalid input."""
    step = libdrm.pipeline.ZipFilesToJSONFiles()
    with pytest.raises(zipfile.BadZipFile):
        next(step.logic([invalid_zipfile]))


def test_ExtractJSONLinesFromJSONFiles_step_with_valid_JSON_file_iterator_fixture(valid_json_files_iterator):
    """Test ZipFilesToJSONFiles Pipeline Step logic with valid JSON files iterator fixture."""
    step = libdrm.pipeline.JSONFilesToJSONLines()
    json_bytes = next(step.logic(valid_json_files_iterator))
    assert json_bytes == {
        "id": "123456789",
        "created_at": "Sat May 15 08:49:13 +0000 2021",
        "text": "A text to be annotated with floods model",
        "lang": "it"
    }


def test_ExtractJSONLinesFromJSONFiles_step_with_invalid_JSON_file_iterator_fixture(invalid_json_files_iterator):
    """Test ZipFilesToJSONFiles Pipeline Step logic with invalid JSON files iterator fixture.
    It raises StopIteration because the iterator is empty.
    The JSON validation try/except in JSONFilesToJSONLines
    catches the invalid bytes line in the JSON file (see conftest.py, line 80)
    TIP:
        run pytest with -s flag to see the dedicated WARNING in the Captured log call.
    """
    step = libdrm.pipeline.JSONFilesToJSONLines()
    with pytest.raises(StopIteration):
        next(step.logic(invalid_json_files_iterator))


def test_JSONLinesToDataPoints_step_with_valid_JSON_lines_iterator_fixture(valid_json_bytes_iterator):
    """Test JSONLinesToDataPoints Pipeline Step logic with valid JSON bytes iterator fixture."""
    step = libdrm.pipeline.JSONLinesToDataPoints()
    data_point = next(step.logic(valid_json_bytes_iterator))
    assert isinstance(data_point, libdrm.pipeline.DisasterModel)


def test_BatchesOfBytes_step_with_valid_JSON_bytes_batches_iterator_fixture(valid_json_bytes_iterator):
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
