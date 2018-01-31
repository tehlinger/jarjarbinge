import unittest
import pprint
from static_commands import *
from traffic_controller import *

class TestDataLoad(unittest.TestCase):

    def setUp(self):
        self.net_cond = {'ul_rat_kb': None, 'dl_rat_kb': None, 'ul_del_ms':
                None, 'dl_del_ms': None, 'ul_jit_ms': None, 'dl_jit_ms': None,
                'ul_los': None, 'dl_los': None}

    def test_netem_cmd(self):
        self.net_cond['ul_del_ms']=50
        self.assertEqual(netem_cmd(True,self.net_cond),
                ['netem', 'delay', '50ms'])
        self.net_cond['ul_jit_ms']=10
        self.assertEqual(netem_cmd(True,self.net_cond),
                ['netem', 'delay', '50ms','10ms','distribution','normal'])
        self.net_cond['ul_jit_ms']=None
        self.net_cond['ul_del_ms']=None
        self.net_cond['ul_los']=0.2
        self.assertEqual(netem_cmd(True,self.net_cond),
                ['netem', 'loss','0.2%'])
        self.net_cond['ul_del_ms']=50
        self.net_cond['ul_jit_ms']=10
        self.assertEqual(netem_cmd(True,self.net_cond),
                ['netem', 'delay',
                    '50ms','10ms','distribution','normal','loss','0.2%',])

    def test_tbf_cmd(self):
        self.net_cond['ul_rat_kb']=50
        self.assertEqual(tbf_cmd(True,self.net_cond),
                ['tbf','rate','50kbit','burst','1kbit','limit','1mbit'])

    def test_get_cmd_list_full(self):
        self.net_cond['ul_rat_kb']=5
        self.net_cond['ul_los']   =50
        self.net_cond['ul_jit_ms']=500
        self.net_cond['ul_del_ms']=5000
        self.net_cond['dl_rat_kb']=10
        self.net_cond['dl_los']   =100
        self.net_cond['dl_jit_ms']=1000
        self.net_cond['dl_del_ms']=10000
        expected = [
                ['tc','qdisc','add','dev','eth1','root','handle','1:',
                    'tbf','rate','5kbit','burst','1kbit','limit','1mbit'],
                ['tc','qdisc','add','dev','eth1','parent','1:1','handle','10:',
                    'netem',
                    'delay','5000ms','500ms','distribution','normal','loss','50%'],
                ['tc','qdisc','add','dev','ifb0','root','handle','1:',
                    'tbf','rate','10kbit','burst','1kbit','limit','1mbit'],
                ['tc','qdisc','add','dev','ifb0','parent','1:1','handle','10:',
                    'netem',
                    'delay','10000ms','1000ms','distribution','normal','loss','100%']
                ]
        result = to_cmd_list(self.net_cond)
        self.assertEqual(expected,result)

    def test_get_cmd_list_ul_only(self):
        self.net_cond['ul_rat_kb']=5
        self.net_cond['ul_los']   =50
        self.net_cond['ul_jit_ms']=500
        self.net_cond['ul_del_ms']=5000
        expected = [
                ['tc','qdisc','add','dev','eth1','root','handle','1:',
                    'tbf','rate','5kbit','burst','1kbit','limit','1mbit'],
                ['tc','qdisc','add','dev','eth1','parent','1:1','handle','10:',
                    'netem',
                    'delay','5000ms','500ms','distribution','normal','loss','50%']
                ]
        result = to_cmd_list(self.net_cond)
        self.assertEqual(expected,result)

    def test_get_cmd_list_no_tbf(self):
        self.net_cond['ul_los']   =50
        self.net_cond['ul_jit_ms']=500
        self.net_cond['ul_del_ms']=5000
        expected = [
                ['tc','qdisc','add','dev','eth1','root','handle','1:',
                    'netem',
                    'delay','5000ms','500ms','distribution','normal','loss','50%']
                ]
        result = to_cmd_list(self.net_cond)
        self.assertEqual(expected,result)

    def test_get_cmd_list_no_netem(self):
        self.net_cond['ul_rat_kb']=5
        expected = [
                ['tc','qdisc','add','dev','eth1','root','handle','1:',
                    'tbf','rate','5kbit','burst','1kbit','limit','1mbit']
                ]
        result = to_cmd_list(self.net_cond)
        self.assertEqual(expected,result)

if __name__ == '__main__':
    unittest.main()

