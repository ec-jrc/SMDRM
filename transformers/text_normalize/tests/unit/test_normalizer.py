import os
import sys
# this allow to import normalize.py module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import normalizer


def test_ampersand_norm(text):
    result = normalizer.ampersand_norm(text)
    assert result == "RT \na text string, and to be normalized @API #NothingSpecial https://example.com http"


def test_anonymize(text):
    result = normalizer.anonymize(text)
    assert result == "RT \na text string,   &amp; to be normalized  #NothingSpecial https://example.com http"


def test_hashtags_norm(text):
    result = normalizer.hashtags_norm(text)
    assert result == "RT \na text string,   &amp; to be normalized @API NothingSpecial https://example.com http"


def test_retweeted_norm(text):
    result = normalizer.retweeted_norm(text)
    assert result == "\na text string,   &amp; to be normalized @API #NothingSpecial https://example.com http"


def test_urls_norm(text):
    result = normalizer.urls_norm(text)
    assert result == "RT \na text string,   &amp; to be normalized @API #NothingSpecial url"


def test_newline_norm(text):
    result = normalizer.newline_norm(text)
    assert result == "RT a text string,   &amp; to be normalized @API #NothingSpecial https://example.com http"


def test_consecutive_whitespace_norm(text):
    result = normalizer.consecutive_whitespace_norm(text)
    assert result == "RT a text string, &amp; to be normalized @API #NothingSpecial https://example.com http"
