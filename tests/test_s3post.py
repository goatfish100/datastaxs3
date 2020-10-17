import json




# Boto3 library generates signed url locally - it has all key's
# it needs and does not contact AWS - thus no need to mock/dummy 
# service

def test_index(app, client):
    res = client.get('/s3post/jls')
    assert res.status_code == 200
    # expected = {'hello': 'world'}
    print(res.get_data(as_text=True))
    assert expected == json.loads(res.get_data(as_text=True))


