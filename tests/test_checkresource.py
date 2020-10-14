import json
import boto3
from mainapp import check_resource

# # def check_resource(bucket_name, object_name, expiration=3600):
# #     print("inside test check_resource")
# #     return True   
# @mock_s3
# def test_check_resource(app, client):
#     res = check_resource('goatfish100', 'jltest', expiration=3600)
#     assert res == True
#     # expected = {'hello': 'world'}
#     # assert expected == json.loads(res.get_data(as_text=True))