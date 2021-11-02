import libdrm.elastic


def test_init_client():
    es = libdrm.elastic.ElasticSearchClient(url="http://localhost:9200")
    assert isinstance(es, libdrm.elastic.ElasticSearchClient)


def test_create_index():
    pass


def test_add_doc():
    pass
