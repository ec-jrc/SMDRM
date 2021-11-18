import requests

api_test_url = "http://text-normalize:15050"


def test_api_get():
    """
    API GET request.
    """
    r = requests.get(api_test_url)
    assert r.status_code == 200
    assert r.json() == {'api_name': 'TextNormalizeAPI', 'resources': ["/", "/normalize"], 'is_alive': True}


def test_api_post(batch_texts):
    """
    API POST request.
    """
    r = requests.post(api_test_url, json={"batch": batch_texts})
    assert r.json() == {
        "text_normalized": [
            "a text string and to be normalized nothingspecial url",
        ]
    }


def test_api_post_bad():
    """
    Bad API POST request.
    """
    r = requests.post(api_test_url, json={"unknown": []})
    assert r.json() == {
        "message": "Missing batch payload."
    }
