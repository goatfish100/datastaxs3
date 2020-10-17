#mport boto3
#mport pytest_localstack
#
#
#ocalstack = pytest_localstack.patch_fixture(
#   services=["s3"],  # Limit to the AWS services you need.
#   scope='module',  # Use the same Localstack container for all tests in this module.
#   autouse=True,  # Automatically use this fixture in tests.
#
#
#ef test_s3_bucket_creation():
#   s3 = boto3.resource('s3')  # Botocore/boto3 will be patched to use Localstack
#   assert len(list(s3.buckets.all())) == 0
#   bucket = s3.Bucket('foobar')
#   bucket.create()
#   assert len(list(s3.buckets.all())) == 1
