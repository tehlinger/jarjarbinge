from http.server import BaseHTTPRequestHandler,HTTPServer
import time
from urllib import parse
from pprint import pprint

def page_write(s,message):
    s.wfile.write(message.encode('utf-8'))

class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()

    def do_POST(s):
        """Response do a GET"""
        content_length = int(s.headers['Content-Length'])
        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        post_data = s.rfile.read(content_length)
        pprint(parse.parse_qs(post_data.decode('utf-8')))

    def do_GET(s):
        """Response do a POST"""
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
        page_write(s,"<html><head><title>Dummy server</title></head>")
        page_write(s,"<body><p>Dumb basic server</p>")
        page_write(s,("<\br><p>You accessed path: </p>"+s.path))
        args = parse.parse_qs(s.path)
        page_write(s,"<\br><p>ARGS : " +str(args)+"</br>")
        page_write(s,"</body></html>")
