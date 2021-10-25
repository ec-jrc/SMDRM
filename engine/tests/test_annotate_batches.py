import pathlib
import sys

from unittest.mock import Mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from start import iter_annotate_batches, requests, apis_by_disaster


def test_iter_batch_annotate_floods(monkeypatch):
    """
    Mock api_annotate() return value.
    The variable `expected` fix the number of batches passed to the annotator API.
    We expect 4 api calls to the floods url, and the batch payload response yielded.
    """
    mocked_response = Mock()
    input_batch = {
        "batch": [
            dict(
                id="123456789",
                created_at="Sat May 15 08:49:13 +0000 2021",
                text="A text to be annotated with floods model",
                lang="it",
                disaster_type="floods",
            )
        ]
        * 2
    }
    expected_calls = 4
    expected_url = apis_by_disaster["floods"]   # http://floods:5001/annotate
    mocked_response.json.return_value = input_batch
    monkeypatch.setattr("requests.post", mocked_response)
    for _ in iter_annotate_batches([input_batch] * expected_calls):
        pass
    # as passed disaster type is floods
    assert requests.post.call_args[0] == (expected_url,)
    # json as in requests.post call
    assert requests.post.call_args[1] == {"json": input_batch}
    assert requests.post.call_count == expected_calls
