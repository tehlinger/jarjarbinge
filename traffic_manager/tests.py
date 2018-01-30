import unittest
import pprint
from static_commands import *

class TestDataLoad(unittest.TestCase):

    def setUp(self):
        self.net_cond = {'ul_rat_kb': None, 'dl_rat_kb': None, 'ul_del_ms':
                None, 'dl_del_ms': None, 'ul_jit_ms': None, 'dl_jit_ms': None,
                'ul_los': None, 'dl_los': None}

    def test_netem_cmd(self):
        self.net_cond['ul_del_ms']=50
        self.assertEqual(netem_cmd("eth0",True,self.net_cond),
                ['netem', 'delay', '50ms'])
        self.net_cond['ul_jit_ms']=10
        self.assertEqual(netem_cmd("eth0",True,self.net_cond),
                ['netem', 'delay', '50ms','10ms','distribution','normal'])
        self.net_cond['ul_jit_ms']=None
        self.net_cond['ul_del_ms']=None
        self.net_cond['ul_los']=0.2
        self.assertEqual(netem_cmd("eth0",True,self.net_cond),
                ['netem', 'loss','0.2%'])
        self.net_cond['ul_del_ms']=50
        self.net_cond['ul_jit_ms']=10
        self.assertEqual(netem_cmd("eth0",True,self.net_cond),
                ['netem', 'delay',
                    '50ms','10ms','distribution','normal','loss','0.2%',])

    def test_tbf_cmd(self):
        self.net_cond['ul_rat_kb']=50



if __name__ == '__main__':
    unittest.main()

