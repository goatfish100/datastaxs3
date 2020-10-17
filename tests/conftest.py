import pytest
import boto3
from mainapp import app as flask_app
from dotenv import load_dotenv, find_dotenv
import os
import logging
from logging.config import fileConfig

load_dotenv(find_dotenv())
AWS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET = os.getenv('AWS_SECRET')
AWS_BUCKET = os.getenv('AWS_BUCKET')
LOGGER = logging.getLogger()
S3_RESOURCE = "s3_RESOURCE.TXT"

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    LOGGER.info("@pytest.fixture")
    print(AWS_KEY)

    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=AWS_BUCKET)
#    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET)
        
#   try:
#       response = s3_client.upload_file(S3_RESOURCE, AWS_BUCKET, S3_RESOURCE)
#   except ClientError as e:
#       logging.error(e)
    
    return app.test_client()
