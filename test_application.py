import datetime
import json
import logging
import os
import unittest
import unittest.mock
from logging.config import fileConfig
from os.path import dirname, join
from unittest.mock import patch


from dotenv import load_dotenv
from flask import Flask, g

from cdrapplication import application
from handlers import HandlerCdr

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


app = Flask(__name__)



class TestHandleCdr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.app = application.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        self.cdr = HandlerCdr("/tmp")
        with open("./test/cdr_inbound.json", "r") as read_file_inbound_good:
            self.datainboundgood = read_file_inbound_good.read()
        with open("./test/cdr_inbound_missing_compact.json", "r") as read_file_inbound_bad:
            self.datainboundmissing = read_file_inbound_bad.read()
        with open("./test/cdr_outbound.json", "r") as read_file_outbound_good:
            self.dataoutboundgood = read_file_outbound_good.read()
        with open("./test/cdr_outbound_missing.json", "r") as read_file_outbound_bad:
            self.dataoutboundmissing = read_file_outbound_bad.read()

         
    # def test_get_progressive_mediasec(self):
    #     result = create_email_intro_msg(jsonres)
    #     self.assertTrue(len(result)>0)
    def test_get_key_time(self):
        time = 1540000000.000000
        timeval5Min = self.cdr.get_key_time(time, '5Min')
        timeval1Hr = self.cdr.get_key_time(time, '1Hr')
        timeval1Day = self.cdr.get_key_time(time, '1Day')

        LOGGER.info(timeval5Min)
        LOGGER.info(timeval1Hr)
        LOGGER.info(timeval1Day)

        self.assertTrue(timeval5Min==1539999900.0)
        self.assertTrue(timeval1Hr==1539997200.0)
        self.assertTrue(timeval1Day==1539993600.0)
        # self.assertRaises(cdr.get_key_time(time, 'BADVAL'))
        with self.assertRaises(KeyError):
            self.cdr.get_key_time(time, 'BADVAL')


    def test_get_progress_mediamsec(self):
        #//content = json.loads(jsoncontent)
        self.assertTrue(self.cdr.get_progress_mediamsec(jsoncontent_test1), jsoncontent_test1['variables']['progress_mediamsec'])
        self.assertTrue(self.cdr.get_progress_mediamsec(jsoncontent_test2), jsoncontent_test2['variables']['progressmsec'])


  
