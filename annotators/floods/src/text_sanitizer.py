import re
import string
import typing


regexp = {
    "ampersand": re.compile(r"\s+&amp;?\s+"),
    "retweet": re.compile(r"^RT @\w+\s?:\s*"),
    "mention": re.compile(r"@[A-Za-z0-9_]+\b"),
    "time_a": re.compile(r"\b\d\d?:\d\d\s*[ap]\.?m\.?\b", flags=re.IGNORECASE),
    "time_b": re.compile(r"\b\d\d?\s*[ap]\.?m\.?\b", flags=re.IGNORECASE),
    "time_c": re.compile(r"\b\d\d?:\d\d\b", flags=re.IGNORECASE),
    "time_d": re.compile(r"\b\d\d?:\d\d:\d\d\b", flags=re.IGNORECASE),
    "url": re.compile(r"\bhttps?:\S+", flags=re.IGNORECASE),
    "broken_url": re.compile(r"\s+https?$", flags=re.IGNORECASE),
    "nochars": re.compile(r'[^\w\d\s:\'",.\(\)#@\?!/’_]+'),
    "newlines": re.compile(r"\n"),
    "double_spaces": re.compile(r"\s{2,}"),
}


def no_punctuation(text: str, punctuation: str = string.punctuation) -> str:
    """Remove the following chars from text:
    !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    """
    return text.translate(str.maketrans("", "", punctuation))


def features_normalizer(text: str) -> str:
    """Twitter features normalization."""
    text = text.lstrip("RT ")
    # Ampersand
    text = regexp["ampersand"].sub(" and ", text)
    # User mentions
    text = regexp["mention"].sub("_USER_", text)
    # Time
    text = regexp["time_a"].sub("_TIME_", text)
    text = regexp["time_b"].sub("_TIME_", text)
    text = regexp["time_c"].sub("_TIME_", text)
    text = regexp["time_d"].sub("_TIME_", text)
    # URLs
    text = regexp["url"].sub("_URL_", text)
    # Broken URL at the end of a line
    text = regexp["broken_url"].sub("_URL_", text)
    # Non-alpha non-punctuation non-digit characters
    text = regexp["nochars"].sub("_URL_", text)
    # Newlines and double spaces
    text = regexp["newlines"].sub(" ", text)
    text = regexp["double_spaces"].sub(" ", text)
    # hashtags
    text = text.replace("#", "")
    return text.strip()


def sanitize(texts: typing.List[str]) -> typing.List[str]:
    normalized = list(map(features_normalizer, texts))
    normalized_clean = list(map(no_punctuation, normalized))
    return normalized_clean
