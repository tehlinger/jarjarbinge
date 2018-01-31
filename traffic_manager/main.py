import argparse
import time
import pprint
import requests
import urllib3
from http.server import BaseHTTPRequestHandler,HTTPServer
import sys

import traffic_controller
from server_code import *

HOST_NAME="127.0.0.1"
PORT_NUMBER=8002

def main():
    server_class = HTTPServer
    HandlerClass = MakeHandlerClassFromArgv(sys.argv)
    httpd = server_class((HOST_NAME, PORT_NUMBER), HandlerClass)
    print(str(time.asctime())+" Server Starts - %s:%s"%(HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server interrupted")
        pass
    HandlerClass.tc.reset_all()
    httpd.server_close()
    print(str(time.asctime())+"Server Stops - %s:%s" %\
            (HOST_NAME, PORT_NUMBER))

if __name__== "__main__":
    main()
