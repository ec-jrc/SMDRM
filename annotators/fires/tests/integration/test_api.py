import requests

api_test_url = "http://fires-test:15002"


def test_api_get():
    """
    API GET request.
    """
    r = requests.get(api_test_url)
    assert r.status_code == 200
    assert r.json() == {'api_name': 'FiresAPI', "resources": ["/", "/annotate"], 'is_alive': True}


def test_api_post():
    """
    API POST request.
    """
    batch = {
        "batch": {
            "lang": "en",
            "texts": [
                "a fires disaster text url",
                "another fires disaster text url",
            ]
        }
    }
    r = requests.post(api_test_url, json=batch)
    expected = {
        "batch": {
            "lang": "en",
            "texts": [
                "a fires disaster text url",
                "another fires disaster text url",
            ],
            "annotation_probs": [
                "0.987922",
                "0.996030",
            ],
            "annotation_type": "fires",
        }
    }
    assert r.json() == expected


def test_api_post_missing_payload():
    """
    Bad API POST request.
    """
    r = requests.post(api_test_url, json={})
    assert r.json() == {"message": "Invalid/missing input payload."}


def test_api_post_missing_texts():
    """
    Bad API POST request.
    """
    r = requests.post(api_test_url, json={"batch": {"lang": "it"}})
    assert r.json() == {"message": "Missing input texts."}
