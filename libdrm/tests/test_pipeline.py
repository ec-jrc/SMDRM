import pathlib
import zipfile

import libdrm.datamodels
import libdrm.pipeline


def test_iter_zip_files(valid_zipfile, invalid_zipfile):
    # skip invalid zip file
    # _file should always be the valid zip file
    for _file in libdrm.pipeline.iter_zip_files([valid_zipfile, invalid_zipfile]):
        assert isinstance(_file, pathlib.Path)
        assert _file == valid_zipfile


def test_iter_zip_file_content(json_files_gen):
    for _file in json_files_gen:
        assert isinstance(_file, zipfile.ZipExtFile)
        assert _file.name == "valid.json"


def test_iter_json_file_content(json_files_gen):
    for data_point in libdrm.pipeline.iter_json_file_content(json_files_gen):
        assert data_point["id"] == 123456789
        assert data_point["disaster_type"] in libdrm.datamodels.disaster.ALLOWED_DISASTER_TYPES
        # added only when JSON data point is serialized
        assert "uploaded_at" in data_point
        assert "text_sanitized" in data_point and isinstance(data_point["text_sanitized"], str)
        assert "annotation" in data_point and isinstance(data_point["annotation"], float)
        assert "img" in data_point and isinstance(data_point["img"], dict)


def test_iter_json_file_content_invalid(valid_zipfile_invalid_json):
    json_files = libdrm.pipeline.iter_zip_file_content([valid_zipfile_invalid_json])
    for data_point in libdrm.pipeline.iter_json_file_content(json_files):
        assert data_point == "this is not JSON!"


def test_iter_in_batch(json_files_gen):
    data_points = libdrm.pipeline.iter_json_file_content(json_files_gen)
    batches = 0
    # format: {"batch": [data_points, ...]}
    for batch in libdrm.pipeline.iter_in_batch(data_points, batch_size=12):
        assert len(batch["batch"]) == 12
        batches += 1
    # 60 data_points / 12 data_point per batch
    assert batches == 5
