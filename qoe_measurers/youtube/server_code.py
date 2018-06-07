from http.server import BaseHTTPRequestHandler,HTTPServer
from pyautogui import click
from pyautogui import moveRel
from subprocess import call
import time
from urllib import parse
from pprint import pprint
from launch_experiment import *
import pprint

#ids = ["AntcyqJ6brc","oFkulzWMotY","x02xX2dv6bQ"]

def page_write(s,message):
    s.wfile.write(message.encode('utf-8'))

def MakeHandlerClassFromArgv(init_args):
    """
    Returns the class (class factory)
    Allows  to add instances var to the class
    """
    class MyHandler(BaseHTTPRequestHandler):

        never_launched = True
        dummy_vid = False

        def __init__(s,*args, **kwargs):
            super(MyHandler, s).__init__(*args, **kwargs)

        def do_HEAD(s,path=None):
            if not path:
                s.send_response(200)
                s.send_header("Content-type","text/html")
                s.end_headers()
            else:
                if path == '/go':
                    MyHandler.dummy_vid = False
                    s.send_response(200)
                    s.send_header("Content-type","text/html")
                    s.end_headers()
                    if MyHandler.never_launched:
                        print("Launching experiment...")
                        launch_experiment(s.get_params())
                        MyHandler.never_launched = False
                if path == '/go_clear':
                    MyHandler.dummy_vid = True
                    s.send_response(200)
                    s.send_header("Content-type","text/html")
                    s.end_headers()
                    if MyHandler.never_launched:
                        print("Launching experiment...")
                        launch_experiment(s.get_params(),go_clear=True)
                        MyHandler.never_launched = False
                if path =="/getVideoID_Res":
                #chrome extension (client) wants data
                #on the video he must play
                    #time.sleep(3)
                    with open("tmp","r") as f:
                        l = f.readlines()[0]
                        if "real" in l:
                           is_dummy = False
                        else:
                            is_dummy = True
                    if is_dummy is not True:
                        vid_id = random.choice(["bUhdSs0VK9c",
                            "im_2tkN4VKY",
                            "O3zza3ofZ0Q",
                            "oFkulzWMotY",
                            "RSzD92Rl8j4",
                            "tSjhLFWj9TU"
                            ])
                    else:
                        vid_id = "RK1K2bCg4J8"
                    print("CHOSEN ID : "+vid_id)
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("videoID",vid_id)
                    s.send_header("resolution","hd1080")
                    s.send_header("videoDuration","30")
                    s.end_headers()
                if path =="/click":
                #chrome extension (client) wants data
                #on the video he must play
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("videoID","oFkulzWMotY")
                    s.send_header("resolution","hd1080")
                    s.send_header("videoDuration","30")
                    s.end_headers()
                    time.sleep(0.8)
                    x = 150
                    #x = 2150
                    y = 150
                    click(x,y,button='right')
                    #time.sleep(1)
                    #click(x,y,button='right')
                    time.sleep(0.1)
                    #Previous player
                    #moveRel(15,222)
                    #HD dezoomed player
                    moveRel(15,180)
                    click()

                if path=="/configureQoS":
                #chrome extention waits for QoE to be modified
                #before playing and modifiying the video
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("QoE","OK")
                    s.end_headers()
                if path=="/results":
                    s.send_response(200)
                    s.send_header("Access-Control-Allow-Origin","*")
                    s.send_header("QoE","OK")
                    s.end_headers()
                    #pprint.pprint(s.get_params())


        def do_POST(s):
            """Response do a POST"""
            s.do_HEAD(s.path)
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

        def get_params(s):
            content_length = int(s.headers['Content-Length'])
            post_data = s.rfile.read(content_length)
            qoe_params = parse.parse_qs(post_data.decode('utf-8'))
            pprint.pprint(qoe_params)
            return qoe_params

    return MyHandler
