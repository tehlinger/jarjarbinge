from http.server import BaseHTTPRequestHandler,HTTPServer
import time
from urllib import parse
import pprint
import requests
import sys
import random

def page_write(self,message):
    self.wfile.write(message.encode('utf-8'))

def get_qos():
    TEST_QOS = \
            {'dl_los': None, 'dl_del_ms': 0, 'ul_rat_kb': None,\
            'ul_jit_ms': None, 'ul_del_ms': None, 'dl_rat_kb': None,\
            'dl_jit_ms': None, 'ul_los': None}
    r1= random.randint(1,3)
    if r1== 1 :
        r1= 0
    if r1== 2:
        r1= random.randint(100,800)/100
    if r1== 3:
         r1= random.randint(900,3000)/100
    r = random.randint(1,3)
    if r == 1 :
        r = random.randint(10,800)
    if r == 2:
        r = random.randint(800,3000)
    if r == 3:
         r = random.randint(3000,30000)
    TEST_QOS['dl_rat_kb'] = r
    TEST_QOS['dl_los'] = r1
    print("======")
    print("DL RATE "+str(TEST_QOS['dl_rat_kb'])+"kbps")
    print("LOSSES "+str(TEST_QOS['dl_los'])+"%")
    return TEST_QOS

def MakeHandlerClassFromArgv(init_args):
    """
    Returns the class (class factory)
    Allows  to add instances var to the class
    """
    class resultsHandler(BaseHTTPRequestHandler):
        must_not_stop = True
        qoe_data = None
        results = None

        def __init__(self,*args, **kwargs):
            super(resultsHandler, self).__init__(*args, **kwargs)

        def _set_headers(self):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                #if path=="/results":

        def do_POST(self):
            """Response do a POST"""
            results = self.get_params()
            #pprint.pprint(results_short(results))
            print("QOE :" +str(results['QoE']))
            print("======")
            self.send_response(200)
            self.send_header("Content-type","application/json")
            self.end_headers()
            resultsHandler.must_not_stop = False
            resultsHandler.results = results

        def get_params(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            qos_params = parse.parse_qs(post_data.decode('utf-8'))
            return qos_params

    return resultsHandler

def results_short(r_dict):
    result = r_dict.copy()
    result['httpInfo'] = ""
    return result

class StoppableHttpServer(HTTPServer):
    def run_while_true(server_class=HTTPServer,
                   handler_class=BaseHTTPRequestHandler):
        """
        This assumes that keep_running() is a function of no arguments which
        is tested initially and after each request.  If its return value
        is true, the server continues.
        """
        server_address = ('', 8000)
        httpd = server_class(server_address, handler_class)
        while handler_class.must_not_stop:
            httpd.handle_request()
        return handler_class.results
