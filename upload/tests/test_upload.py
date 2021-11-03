import requests

upload_api_url = "http://upload-test:15000"


def test_api_get():
    """
    Upload API GET request.
    Successful response: {'api_name': 'UploadAPI', 'resource': '/upload', 'is_alive': True}
    """
    r = requests.get(upload_api_url)
    assert r.status_code == 200
    assert r.json() == {'api_name': 'UploadAPI', 'resource': '/upload', 'is_alive': True}


def test_api_post():
    """
    Upload API POST request.
    Successful response: {"status": "uploaded", "meta": meta, "stand_alone": True}
    Engine API is not required for this test. Hence, we skip the request with the --stand-alone flag (api.py)
    """
    with open('test_data.zip', 'rb') as f:
        r = requests.post(upload_api_url, files={"zip_file": f})
    assert r.json() == {
        'status': 'uploaded',
        'meta': {
            'floods_annotator': False,
            'fires_annotator': False
        },
        'stand_alone': True
    }


def test_api_post_with_meta():
    """
    Upload API POST request with metadata.
    Successful response: {"status": "uploaded", "meta": meta, "stand_alone": True}
    Engine API is not required for this test. Hence, we skip the request with the --stand-alone flag (api.py)
    """
    with open('test_data.zip', 'rb') as f:
        r = requests.post(upload_api_url, files={"zip_file": f}, data={"floods_annotator": 1})
    assert r.json() == {
        'status': 'uploaded',
        'meta': {
            'floods_annotator': True,
            'fires_annotator': False
        },
        'stand_alone': True
    }
