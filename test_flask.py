import unittest
import unittest.mock
from unittest.mock import patch
from handlers import HandlerCdr
import datetime
import logging
import json 
import redis
import psycopg2
import os
from cdrapplication import application
from logging.config import fileConfig
from os.path import dirname, join
from dotenv import load_dotenv

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
jsoncontent_test1 = {"variables": {"progress_mediamsec": "1370","progressmsec": "0"}}
jsoncontent_test2 = {"variables": {"progress_mediamsec": "0","progressmsec": "1234"}}

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
HTTP_PORT = int(os.getenv('HTTP_PORT'))
DB_CONN = os.getenv('DB_CONN')
ENVIRONMENT = os.getenv('ENVIRONMENT')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

# # Connect to Postgres and Redis
# redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
# pg_conn = psycopg2.connect(DB_CONN)

# cdr = HandlerCdr("/tmp", pg_conn, redis_conn)

class TestFlask(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 
    
    def setUp(self):
        self.app = application.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass
            
    def test_get(self):
        print("runnint test_get")
        result = self.app.get('/test')
        self.assertEqual(result.status_code, 200) 

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestFlask('test_get'))
    suite.addTest(TestHandleCdr('get_key_time'))
    suite.addTest(TestHandleCdr('get_progress_mediamsec'))

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
