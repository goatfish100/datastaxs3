import json

#A good resource
def test_index(app, client):
    res = client.get('/s3geturl/jltest')
    assert res.status_code == 200
    # expected = {'hello': 'world'}
    # assert expected == json.loads(res.get_data(as_text=True))

#A bad resource
def test_index(app, client):
    res = client.get('/s3geturl/abadresource')
    assert res.status_code == 200
    # expected = {'hello': 'world'}
    # assert expected == json.loads(res.get_data(as_text=True))   