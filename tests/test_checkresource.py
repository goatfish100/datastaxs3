import json
import pytest_localstack

localstack = pytest_localstack.patch_fixture(
    services=["s3"],  # Limit to the AWS services you need.
    scope='module',  # Use the same Localstack container for all tests in this module.
    autouse=True,  # Automatically use this fixture in tests.
)

def test_check_resource(app, client):
    res = check_resource('goatfish100', 'jltest', expiration=3600)
    assert res == True
    # expected = {'hello': 'world'}
    # assert expected == json.loads(res.get_data(as_text=True))
