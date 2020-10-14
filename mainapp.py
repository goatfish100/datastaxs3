import logging
import json
import uuid
import os
from logging.config import fileConfig
from dotenv import load_dotenv, find_dotenv
import boto3
from botocore.exceptions import ClientError
from flask import Flask
from flask import request
from flask import jsonify

# load env variables from .env file
load_dotenv(find_dotenv())
AWS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET = os.getenv('AWS_SECRET')
AWS_BUCKET = os.getenv('AWS_BUCKET')

# Set up the logging
fileConfig('logging_config.ini')
LOGGER = logging.getLogger()

app = Flask(__name__)


@app.route('/s3post')
@app.route('/s3post/<filename>')
def s3post(filename):
    # - demo getting unique resource name - but demo purposes not going full 
    # - uuid
    pyuuid = filename+str(uuid.uuid1())[-4:]
    url = create_presigned_post(AWS_BUCKET, pyuuid)
    LOGGER.info(url)
    data = {'posturl': url, 'uuid': pyuuid}
    return jsonify(data), 200

@app.route('/s3check')
@app.route('/s3check/<filename>')
def s3check( filename):
    LOGGER.info("s3check")
    LOGGER.info(filename)

    if check_resource(AWS_BUCKET, filename) == True:
        return jsonify({'ready': 'True'})
    else:
        return jsonify({'ready': 'False'})

@app.route('/s3geturl')
@app.route('/s3geturl/<resourcename>')
def s3geturl( resourcename):
    LOGGER.info("s3geturl")
    LOGGER.info(resourcename)
    timeout = request.args.get('timeout')
    LOGGER.info(timeout)

    url = create_presigned_url(AWS_BUCKET, resourcename, timeout)
    if url !=  None:
        return jsonify({'url': url})
    else:
        return jsonify({'error': 'Not Found'})

@app.route('/hello')
def index():
    return jsonify({'hello': 'world'})

# Standard code to generate resource in boto3 
def create_presigned_url(bucket_name, object_name, expiration=3600):
    # Generate a presigned URL for the S3 object
    if check_resource == False:
        response = jsonify({'error': 'not available'})
        return response
    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response

# No great way to check if resource has been completed uploaded
# Could use S3 to send message to message que - but that could take up to a minute
def check_resource(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET)

    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
    except ClientError:
        pass
        return False
    return True    


def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET)

    try:
        response = s3_client.generate_presigned_url( ClientMethod='put_object',
                                                     Params={'Bucket': AWS_BUCKET, 'Key': object_name},
                                                     ExpiresIn=expiration,)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response
# Run app locally - if not using WSGI server (in dev mode)
if __name__ == "__main__":
    app.run(debug=True)    
