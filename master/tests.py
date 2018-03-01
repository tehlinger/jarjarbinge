import unittest
import pickle
import datetime
import pprint
import pymongo
import filecmp
import os
import json

from mos_p_1203 import *
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

class TestDataLoad(unittest.TestCase):

    def setUp(self):
        self.dic = pickle.load(open("res_1.pck","rb"))

    def test_load_js(self):
        dic_for_mos = prepare_json_for_mos(self.dic)
        expected = json.load(open("expected.json","rb"))
        self.assertEqual(dic_for_mos,expected)

if __name__ == '__main__':
    unittest.main()
