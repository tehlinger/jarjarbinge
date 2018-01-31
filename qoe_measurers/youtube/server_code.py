from http.server import BaseHTTPRequestHandler,HTTPServer
import time
from urllib import parse
from pprint import pprint
from launch_experiment import *
import pprint

def page_write(s,message):
    s.wfile.write(message.encode('utf-8'))

def MakeHandlerClassFromArgv(init_args):
    """
    Returns the class (class factory)
    Allows  to add instances var to the class
    """
    class MyHandler(BaseHTTPRequestHandler):

        never_launched = True

        def __init__(s,*args, **kwargs):
            super(MyHandler, s).__init__(*args, **kwargs)

        def do_HEAD(s,path=None):
            if not path:
                s.send_response(200)
                s.send_header("Content-type","text/html")
                s.end_headers()
            else:
                if path =="/getVideoID_Res":
                #chrome extension (client) wants data
                #on the video he must play
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("videoID","oFkulzWMotY")
                    s.send_header("resolution","hd720")
                    s.send_header("videoDuration","30")
                    s.end_headers()
                if path=="/configureQoS":
                #chrome extention waits for QoE to be modified
                #before playing and modifiying the video
                    #configNetworkQoS()
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("QoE","OK")
                    s.end_headers()
                if path=="/results":
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("QoE","OK")
                    s.end_headers()
                    pprint.pprint(s.get_params())


        def do_POST(s):
            """Response do a POST"""
            s.do_HEAD(s.path)
            if MyHandler.never_launched:
                launch_experiment(s.get_params())
                MyHandler.never_launched = False

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

        def get_params(s):
            content_length = int(s.headers['Content-Length'])
            post_data = s.rfile.read(content_length)
            qoe_params = parse.parse_qs(post_data.decode('utf-8'))
            pprint.pprint(qoe_params)
            return qoe_params

    return MyHandler
