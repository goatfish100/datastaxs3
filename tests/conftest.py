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

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    LOGGER.info("@pytest.fixture")
    print(AWS_KEY)
    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET)
    return app.test_client()
