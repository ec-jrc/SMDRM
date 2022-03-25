import os
import requests
import pytest
from io import BytesIO
from werkzeug.datastructures import FileStorage

# mock POST request
class TestResponse:
    def json(self):
        return {"airflow": "dagrun"}

def mocked_airflow_dagrun_post(*args, **kwargs):
    return TestResponse()

def test_max_content_length_app_config(app):
    '''Test if app is configured with the correct number of bytes for MAX_CONTENT_LENGTH var'''
    assert app.config["MAX_CONTENT_LENGTH"] == 1000

def test_upload(client, monkeypatch):
    '''Test if upload endpoint send POST request to Airflow API and receive expected output'''

    # mock input
    mocked_zipfile = FileStorage(
        stream=BytesIO(b'anything'),
        filename="test.zip",
        content_type="application/zip",
    )

    # prepare requests data
    data = {"file": mocked_zipfile}
    query_string = "?dag_id=test&collection_id=42"

    # apply the monkeypatch to requests.post to mock the response payload
    monkeypatch.setattr(requests, "post", mocked_airflow_dagrun_post)

    # test file upload
    res = client.post(
            "/api/v1/uploads/upload/"+query_string,
            content_type='multipart/form-data',
            data=data,
        )
    assert res.json == {'filename': 'test.zip', 'airflow_response': {'airflow': 'dagrun'}}

def test_upload_with_invalid_content_type(client, monkeypatch):
    '''Test if upload endpoint fails when sending POST request to Airflow API with invalid content type'''

    # mock invalid input
    mocked_zipfile = FileStorage(
        stream=BytesIO(b'wrong content type'),
        filename="test.json",
        content_type="application/json",
    )

    # prepare requests data
    data = {"file": mocked_zipfile}
    query_string = "?dag_id=test&collection_id=42"

    # apply the monkeypatch to requests.post to mock the response payload
    monkeypatch.setattr(requests, "post", mocked_airflow_dagrun_post)

    # test file upload
    res = client.post(
            "/api/v1/uploads/upload/"+query_string,
            content_type='multipart/form-data',
            data=data,
        )
    assert res.status_code == 415, 'Expected error code is 415 for "content_type" != "application/zip"'

def test_upload_with_exceeded_content_length(client):
    '''Test if upload endpoint fails when sending oversized files'''

    # mock oversize file content length
    oversized_bytes = b'oversized upload'*100
    # max content length for tests in 1000 bytes
    assert len(oversized_bytes) > 1000, "content length of the uploaded file should be above the MAX_CONTENT_LENGTH limit (1000 bytes)"

    # mock invalid input
    mocked_zipfile = FileStorage(
        stream=BytesIO(oversized_bytes),
        filename="test.zip",
        content_type="application/zip",
    )

    # prepare requests data
    data = {"file": mocked_zipfile}
    query_string = "?dag_id=test&collection_id=42"

    # test file upload
    res = client.post(
            "/api/v1/uploads/upload/"+query_string,
            content_type='multipart/form-data',
            data=data,
        )
    
    # mocking requests.post is not required for this test because
    # the content_length is checked prior to sending the POST request
    assert res.status_code == 413, "RequestEntityTooLarge exception (413) should occur when uploading files larger than the MAX_CONTENT_LENGTH limit (1000 bytes)"

def test_upload_list(client, monkeypatch):
    '''Test if uploads endpoint get uploaded files from uploads directory'''

    expected = ["test1.zip", "test2.zip"]
    def mocked_listdir(*args, **kwargs):
        return expected

    # apply the monkeypatch to os.listdir to mock the response payload
    monkeypatch.setattr(os, "listdir", mocked_listdir)
    
    res = client.get("/api/v1/uploads/")
    assert res.status_code == 200
    assert res.json == expected
