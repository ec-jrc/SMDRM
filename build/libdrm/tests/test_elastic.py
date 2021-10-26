import libdrm.elastic


def test_init_client():
    es = libdrm.elastic.ElasticSearchClient(
        url="http://localhost:9200", index="smdrm-test"
    )
    assert isinstance(es, libdrm.elastic.ElasticSearchClient)
    assert str(es) == "ElasticSearchClient(url=http://localhost:9200)"


def test_create_index():
    pass


def test_add_doc():
    pass
