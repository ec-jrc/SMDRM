import os
import requests
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src import transformations


texts = [
    "Un texte d`information sur Rio de Janeiro, écrit à Paris.",
    "a text in english without place candidates.",
    "ed uno in italiano da Roccacannuccia nella pianura pontina"
]

# deeppavlov model output
y_hat = [
    [
        ["Un", "texte", "d", "`", "information", "sur", "Rio", "de", "Janeiro", ",", "\u00e9crit", "\u00e0", "Paris", "."],
        ["O", "O", "O", "O", "O", "O", "B-GPE", "I-GPE", "I-GPE", "O", "O", "O", "B-GPE", "O"],
    ],
    [
        ["a", "text", "in", "english", "without", "place", "candidates", "."],
        ["O", "O", "O", "B-LANGUAGE", "O", "O", "O", "O"],
    ],
    [
        ["ed", "uno", "in", "italiano", "da", "Roccacannuccia", "nella", "pianura", "pontina"],
        ["O", "B-CARDINAL", "O", "B-LANGUAGE", "O", "B-LOC", "I-LOC", "I-LOC", "I-LOC"],
    ],
]

allowed_tags = ["B-GPE", "I-GPE", "B-FAC", "I-FAC", "B-LOC", "I-LOC"]


# custom class to be the mock return value
# will override the requests.Response returned from requests.post
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return y_hat


def test_tag_with_mult_bert(monkeypatch):
    """Test if API call to DeepPavlov returns the expected payload."""
    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_post(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "post", mock_post)

    result = transformations.tag_with_mult_bert(texts)
    assert result == y_hat


def test_extract_place_candidates():
    """Test if extract_place_candidates returns the correct places wrt the allowed tags for each texts."""
    expected = [["Rio de Janeiro", "Paris"], [], ["Roccacannuccia nella pianura pontina"]]
    places = transformations.extract_place_candidates(y_hat, allowed_tags)
    assert places == expected


def test_normalize_places():
    """Test if normalize_places returns the normalized texts i.e. _loc_ tag for each recognized place candidate."""
    places = transformations.extract_place_candidates(y_hat, allowed_tags)
    result = list(transformations.normalize_places(texts, places))
    expected = [
        'Un texte d`information sur _loc_, écrit à _loc_.',
        'a text in english without place candidates.',
        'ed uno in italiano da _loc_'
    ]
    assert result == expected


def test_apply_transformations():
    """Test if apply transformations return the input text transformed as expected."""
    text = "@Toroloco Nos nos \\ 'vemos' @ 12:12 a.m. or 1 pm or 12:05:06 or 13:33 en \"\" la SB Nick &amp; CIA... _loc_ #RunToMiami #SBLIV #100Yardas #Yarders #NFL 🏈🏈🏈 https://t.co/nVdULr6JXG,     badurl  https://...."
    result = transformations.apply_transformations(text)
    expected = "nos nos vemos   or or or en la sb nick and cia  runtomiami sbliv 100yardas yarders nfl  badurl   _urlincl_ _locincl_"
    assert result == expected