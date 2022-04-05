def test_health(client):
    res = client.get('api/v1/info/health')
    assert res.status_code == 200
    assert res.json == ["OK"]
