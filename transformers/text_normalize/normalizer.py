"""
Normalize raw text data.
"""

import re
import string
import typing


# compiled regex patterns
# An ampersand becomes ` and `
ampersand_pattern = re.compile(r"\s+&amp;?\s+")
# user mentions anonymize
user_mention_pattern = re.compile(r"@[A-Za-z0-9_]+\b")
# Time formats is removed
datetimes_pattern = re.compile(r"\b\d\d?:\d\d\s*[ap]\.?m\.?\b|\b\d\d?\s*[ap]\.?m\.?\b|\b\d\d?:\d\d\b|\b\d\d?:\d\d:\d\d\b", flags=re.IGNORECASE)
# Two (or more) consecutive whitespace characters become one
consecutive_whitespaces_pattern = re.compile(r"\s{2,}")
# New lines
new_line_pattern = re.compile(r"\n")
# Remove Retweet (Twitter exclusive)
retweeted_pattern = re.compile(r"^RT ")
# valid and truncated urls (i.e. end of string)
urls_pattern = re.compile(r"\s+https?$|\bhttps?:\S+", flags=re.IGNORECASE)


def ampersand_norm(text: str):
    """Normalize ampersand feature."""
    return ampersand_pattern.sub(" and ", text)


def anonymize(text: str):
    """Remove User name from text to maintain anonymity."""
    return user_mention_pattern.sub("", text)


def consecutive_whitespace_norm(text: str):
    """Remove/normalize two+ consecutive whitespaces.
    Better kept as last normalization to clean spaces created by previous normalizations."""
    return consecutive_whitespaces_pattern.sub(" ", text)


def datetime_norm(text: str):
    """Remove datetime features from text."""
    return datetimes_pattern.sub("", text)


def hashtags_norm(text: str):
    """Remove pound (#) to normalize hashtag feature into token."""
    return text.replace('#', '')


def punctuation_norm(text: str) -> str:
    """Remove punctuation chars from text."""
    return text.translate(str.maketrans('', '', string.punctuation))


def newline_norm(text: str):
    """Normalize text into a one line string."""
    return new_line_pattern.sub("", text)


def retweeted_norm(text: str):
    """Remove retweeted feature."""
    return retweeted_pattern.sub("", text)


def urls_norm(text: str):
    """Remove/normalize URLs features from text.
    Append `url` feature at the end of the returned string if URLs."""
    return urls_pattern.sub("", text) + "url" if urls_pattern.search(text) else text


def batch_normalize(texts: typing.List[str]) -> typing.List[str]:
    """Apply normalization textual features such as URLs, Hashtags, and others
    commonly present in social media content like Twitter."""
    normalizations = [
        ampersand_norm,
        anonymize,
        datetime_norm,
        hashtags_norm,
        newline_norm,
        retweeted_norm,
        urls_norm,
        # cleanup steps are last
        punctuation_norm,
        consecutive_whitespace_norm,
    ]
    tmp = texts
    for normalization in normalizations:
        tmp = map(normalization, tmp)
    # strip, lower, and return
    return [t.strip().lower() for t in tmp]
