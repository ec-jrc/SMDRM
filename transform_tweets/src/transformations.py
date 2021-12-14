import os
import re
import json
import string
import requests
import typing as t


# development flag
development = bool(int(os.getenv("DEVELOPMENT", 0)))


def tag_with_mult_bert(texts: list) -> requests.Response:
    """DeepPavlov Named Entity Recognition REST API call to tag a list of texts."""
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    # set url wrt the environment
    host = "localhost" if development else "deeppavlov"
    url = "http://{host}:5000/model".format(host=host)
    data = json.dumps({"x": texts})
    r = requests.post(url, headers=headers, data=data)
    return r.json()


def extract_place_candidates(ner_output: t.List[list], allowed_tags: t.List[str]) -> t.List[list]:
    """Extract place candidates given a set of tags allowed by the user."""
    places = []
    for row in (list(zip(tokens, tags)) for tokens, tags in ner_output):
        subset = []
        place_candidate = ""
        for token, tag in row:
            # skip unwanted tags
            if tag not in allowed_tags:
                # leaves us with B-, and I- for all allowed tags
                continue
            if "B-" in tag:
                if place_candidate:
                    # when a new B-egin occurs in the same row
                    # place candidate is not empty
                    # so cache the current place candidate in subset
                    subset.append(place_candidate)
                # first token is always a B-egin tag
                place_candidate = token
                continue
            # subsequent allowed tags are I-inside tags
            place_candidate += " "+token
        # append any residual place candidate
        if place_candidate:
            subset.append(place_candidate)
        places.append(subset)
    return places


def normalize_places(texts: t.List[str], places: t.List[list]) -> t.Iterable[str]:
    for text, place in zip(texts, places):
        tmp = text
        if place:
            for name in place:
                tmp = tmp.replace(name, "_LOC_")
        yield tmp


# non natural language compiled regex
ampersand = re.compile(r'\s+&amp;?\s+')
user_mentions = re.compile(r'@[A-Za-z0-9_]+\b')
datetimes = re.compile(r"\b\d\d?\s*[ap]\.?m\.?\b|\b\d\d?:\d\d\s*[ap]\.?m\.?\b|\b\d\d?:\d\d:\d\d\b|\b\d\d?:\d\d\b", flags=re.IGNORECASE)
url = re.compile(r"\bhttps?:\S+", flags=re.IGNORECASE)
url_broken = re.compile(r"\s+https?$", flags=re.IGNORECASE)
special_chars = re.compile(r'[^\w\d\s:\'",.\(\)#@\?!\/’_]+')
more_than_two_whitespaces = re.compile(r'\s{2,}')


def normalize_ampersand(text: str) -> str:
    return ampersand.sub(" and ", text)


def anonymize(text: str) -> str:
    return user_mentions.sub(" ", text)


def remove_datetimes(text: str) -> str:
    return datetimes.sub(" ", text)


def normalize_url(text: str) -> str:
    return url.sub(" _url_ ", text)


def normalize_url_broken(text: str) -> str:
    return url_broken.sub(" _url_", text)


def normalize_new_lines(text: str) -> str:
    return text.replace('\n', ' ').replace('\r', '')


def remove_special_chars(text: str) -> str:
    return special_chars.sub("", text)


def remove_quotes(text: str) -> str:
    return text.replace("'", "").replace('"', "")


def remove_backslashes(text: str) -> str:
    return text.replace("\\", "")


def normalize_hashtags(text: str) -> str:
    return text.replace("#", "")


def normalize_more_than_two_whitespaces(text: str) -> str:
    return more_than_two_whitespaces.sub(" ", text)


def merge_duplicated_normalization_tags(text: str) -> str:
    """Remove duplicate normalization tags,
    and place only one at the end of the input text."""
    if '_url_' in text:
        text = text.replace('_url_', '') + " _urlincl_"
    if '_loc_' in text:
        text = text.replace('_loc_', '') + " _locincl_"
    return text


def remove_punctuation(text: str, punctuation: str = None) -> str:
    """Remove !"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ from text.
    Notes: underscores are required to highlight normalization tags."""
    punct = punctuation or string.punctuation.replace("_", "")
    return text.translate(str.maketrans("", "", punct))


def group_similar_words(text: str) -> str:
    words = text.split()
    gr_text=[]
    gr_text.append(words[0])
    for i in range(1,len(words)):
        if words[i] == words[i-1]:
            continue
        else:
            gr_text.append(words[i])
    return ' '.join(gr_text)


def apply_transformations(text: str) -> str:
    funcs = [
        normalize_ampersand,
        anonymize,
        remove_datetimes,
        normalize_url,
        normalize_url_broken,
        normalize_new_lines,
        remove_special_chars,
        remove_quotes,
        remove_backslashes,
        normalize_hashtags,
        normalize_more_than_two_whitespaces,
        merge_duplicated_normalization_tags,
        remove_punctuation,
        #group_similar_words,
    ]
    tmp = text
    for func in funcs:
        tmp = func(tmp)
    return tmp.strip().lower()
