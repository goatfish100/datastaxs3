import json

# Boto3 library generates signed url locally - it has all key's
# it needs and does not contact AWS - thus no need to mock/dummy 
# service
#A good resource
def test_index(app, client):
    res = client.get('/s3geturl/jltest')
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True))

