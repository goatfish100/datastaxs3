import json
import logging
import os
from logging.config import fileConfig

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request

from handlers import HandlerCdr

application = Flask(__name__)

# load env variables from .env file
load_dotenv(find_dotenv())


HTTP_PORT = int(os.getenv('HTTP_PORT'))
AWS_KEY = int(os.getenv('HTTP_PORT'))
AWS_SECRET = int(os.getenv('HTTP_PORT'))

# Connect to Postgres and Redis
# Set up logger - reading it's ini file
fileConfig('logging_config.ini')
LOGGER = logging.getLogger()
LOGGER.info('starting cdr processing application on port %s', HTTP_PORT)

application = Flask(__name__)


@application.before_request
def before_request():

    @application.route('/s3put', methods=['POST'])
    def inroutine():
        LOGGER.debug("postJsonHandler() called")
        LOGGER.debug(request)
        return '{"success": true}'


@application.route('/gets3', methods=['GET'])
def heartbeat():
    return '{"success": "true"}'


if __name__ == '__main__':
    # IF set to dev - create dev server for development
    if (ENVIRONMENT == 'dev'):
        LOGGER.info("Environment Dev - using Flask's NON PRODUCTION Server")
        LOGGER.info("DO NOT RUN IN PRODUCTION with this configuration")
        LOGGER.info("http port:" + str(HTTP_PORT))
        application.run(host='localhost', port=HTTP_PORT)
# For Production - launch with
# gunicorn - #gunicorn -w 4 -b localhost:8001 wsgi
