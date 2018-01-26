#Source : https://wiki.python.org/moin/BaseHttpServer

from http.server import BaseHTTPRequestHandler,HTTPServer
import time
from urllib import parse
import pprint

HOST_NAME="127.0.0.1"
PORT_NUMBER=8000

def page_write(s,message):
    s.wfile.write(message.encode('utf-8'))

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()

    def do_GET(s):
        """Response do a GET"""
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
        page_write(s,"<html><head><title>Dummy server</title></head>")
        page_write(s,"<body><p>Dumb basic server</p>")
        page_write(s,("<\br><p>You accessed path: </p>"+s.path))
        args = parse.parse_qs(s.path)
        page_write(s,"<\br><p>ARGS : " +str(args)+"</br>")
        page_write(s,"</body></html>")

def main():
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(str(time.asctime())+" Server Starts - %s:%s"%(HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server interrupted")
        pass
    httpd.server_close()
    print(str(time.asctime())+"Server Stops - %s:%s" %\
            (HOST_NAME, PORT_NUMBER))

if __name__== "__main__":
    main()

