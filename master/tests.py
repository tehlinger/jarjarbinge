import unittest
import datetime
import pprint
import pymongo
from config_loader import *

class TestDataLoad(unittest.TestCase):

    def setUp(self):
      self.test_file="qoe_requests_files/default.json"
      self.test_list_file="qoe_requests_files/default_list.json"
      self.expected_conf={ \
              "service":"DEFAULT","bitrate_Kbps":"500",\
              "duration_ms":"100000"}

    def test_load_js(self):
        self.assertEqual(self.expected_conf,load_qoe_req(self.test_file))

    def test_load_qoe_conf_list(self):
      expected_conf2={ \
         "service":"DEFAULT","bitrate_Kbps":"1000",\
         "duration_ms":"200000"}
      conf_list=[self.expected_conf,expected_conf2]
      self.assertEqual(conf_list,load_qoe_req(self.test_list_file))

if __name__ == '__main__':
    unittest.main()
