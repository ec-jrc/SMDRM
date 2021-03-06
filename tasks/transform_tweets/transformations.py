import os
import re
import json
import pandas
import string
import requests
import typing


# typing
pandas_series = pandas.core.series.Series
pandas_df = pandas.core.frame.DataFrame


def tag_with_mult_bert(texts: list) -> requests.Response:
    """DeepPavlov Named Entity Recognition REST API call to tag a list of texts."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    # API url from within the (default) Docker networks created with docker-compose
    url = "http://{host}:{port}/{endpoint}".format(
        host="deeppavlov", port=5000, endpoint="model/annotate"
    )
    r = requests.post(url, headers=headers, data=json.dumps({"texts": texts}))
    return r.json()


def extract_place_candidates(
    y_hat: typing.List[list], allowed_tags: typing.List[str]
) -> dict:
    """Extract place candidates given a set of tags allowed by the user."""

    place_candidates = list()
    tokens, tags = y_hat

    for index in range(len(tags)):
        candidates = dict()
        curr_tags = tags[index]
        curr_tokens = tokens[index]

        for tag_id, tag in enumerate(curr_tags):

            # place candidates always begin with B-<tag>
            if "B-" in tag:
                _, tag_type = tag.split("-")

                # create a dictionary for this tag
                if tag in allowed_tags and tag_type not in candidates:
                    candidates[tag_type] = list()

                # rebuild the place candidate using I-inside tags
                # that come after the current B-<tag>
                subset = []
                future_tags = curr_tags[tag_id:]
                for ftid, future_tag in enumerate(future_tags, start=tag_id):
                    # break place candidate rebuilding when an unknown tag is reached
                    if future_tag not in allowed_tags:
                        break
                    # token is a substring of place candidate
                    token = curr_tokens[ftid]
                    # non-alphanumeric strings might be wrongly tagged
                    if not token.isalnum():
                        continue
                    subset.append(token)

                # subset exists if place candidates are found
                if subset:
                    candidates[tag_type].append(" ".join(subset))
        place_candidates.append({"candidates": candidates or None})
    return place_candidates


def normalize_places(text: str, place_candidates: dict) -> str:
    """Normalize identified place candidates with common _loc_ tag."""
    if not place_candidates:
        return text
    for tag, names in place_candidates.items():
        for name in names:
            text = text.replace(name, "_loc_")
    return text


# non natural language compiled regex
ampersand = re.compile(r"\s+&amp;?\s+")
user_mentions = re.compile(r"@[A-Za-z0-9_]+\b")
datetimes = re.compile(
    r"\b\d\d?\s*[ap]\.?m\.?\b|\b\d\d?:\d\d\s*[ap]\.?m\.?\b|\b\d\d?:\d\d:\d\d\b|\b\d\d?:\d\d\b",
    flags=re.IGNORECASE,
)
url = re.compile(r"\bhttps?:\S+", flags=re.IGNORECASE)
url_broken = re.compile(r"\s+https?$", flags=re.IGNORECASE)
special_chars = re.compile(r'[^\w\d\s:\'",.\(\)#@\?!\/???_]+')
more_than_two_whitespaces = re.compile(r"\s{2,}")


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


def remove_retweet_flag(text: str) -> str:
    return text.lstrip("RT ")


def normalize_new_lines(text: str) -> str:
    return text.replace("\n", " ").replace("\r", "")


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
    if "_url_" in text:
        text = text.replace("_url_", "") + " _urlincl_"
    if "_loc_" in text:
        text = text.replace("_loc_", "") + " _locincl_"
    return text


def remove_punctuation(text: str, punctuation: str = None) -> str:
    """Remove !"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ from text.
    Notes: underscores are required to highlight normalization tags."""
    punct = punctuation or string.punctuation.replace("_", "")
    return text.translate(str.maketrans("", "", punct))


def group_similar_words(text: str) -> str:
    words = text.split()
    gr_text = []
    gr_text.append(words[0])
    for i in range(1, len(words)):
        if words[i] == words[i - 1]:
            continue
        else:
            gr_text.append(words[i])
    return " ".join(gr_text)


def apply_transformations(text: str) -> str:
    funcs = [
        normalize_ampersand,
        anonymize,
        remove_datetimes,
        normalize_url,
        normalize_url_broken,
        normalize_new_lines,
        remove_retweet_flag,
        remove_special_chars,
        remove_quotes,
        remove_backslashes,
        normalize_hashtags,
        normalize_more_than_two_whitespaces,
        merge_duplicated_normalization_tags,
        remove_punctuation,
        # group_similar_words,
    ]
    tmp = text
    for func in funcs:
        tmp = func(tmp)
    return tmp.strip().lower()
