# -*- coding: utf-8 -*-

import pytest
from libdrm.db import elasticsearch


def test_init_client():
    es = elasticsearch.ElasticSearchClient(
        host="localhost", port=19200, index="smdrm-test"
    )
    assert es.url == "http://localhost:19200/smdrm-test"


def test_create_index():
    pass


def test_add_doc():
    pass
