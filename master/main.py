import argparse
import random
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import time
import pprint
import requests
import urllib3
import server_code
import sys

from qos_selector import *
from config_loader import *

HOST_NAME="127.0.0.1"
PORT_NUMBER = 8000
RESULTS = "results/grid_random_beta.csv"
qos_metrics = \
                ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms', 'ul_del_ms',
                        'dl_rat_kb', 'dl_jit_ms', 'ul_los']
qoe_metrics = \
['QoE', 'availableQualityLevels', 'bufferSizeWhenStart', 'clen_audio',
'clen_video', 'dur', 'getVideoLoadedFraction', 'httpInfo', 'join_time',
'player_load_time', 'resolution', 'stallingNumber', 'timeout',
'totalStallDuration', 'ts_firstBuffering', 'ts_onPlayerReadyEvent',
'ts_onYTIframeAPIReady', 'ts_startPlaying', 'ts_start_js','bitrate_switch']

def header_line():
    r = ""
    for m in qos_metrics:
        r+= m + ","
    for m in qoe_metrics:
        r+= m + ","
    return r

def line_out_of_dict(d,keys):
    r = ""
    for k in keys:
        if k in d:
            value = d[k]
            if k == 'availableQualityLevels':
                r += ','
            else:
                if value == None:
                    value = ''
                else:
                    if type(value) is list and len(value) == 1\
                            and ',' not in value:
                        value = value[0]
                    try:
                        value  = float(value)
                    except:
                        value = value
                r += str(value)+','
        else:
            r += ","
    return r[:-1]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('qoe_file',help="Filepath to qoe_configs")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                                action="store_true")
    args = parser.parse_args()
    return args

def main():
    server_class = server_code.StoppableHttpServer
    args = get_args()
    verbose = args.verbose
    not_interrupted = True
    qos_selector = QosSelector(10)
    while not_interrupted:
        try:
            qos = qos_selector.random_point_in_finite_space()
            #Following are line to get a static qos conf
            qos = QosSelector.get_clear_qos()
            qos['dl_rat_kb'] = 50000
            print("=================================")
            print("QOS : ")
            print(qos)
            r = requests.post("http://127.0.0.1:8002/",data=qos)
            print("Sent QoS request")
            qos_response  = r.content.decode('utf-8')
            qos_response  = json.loads(r.content.decode('utf-8'))
            qoe_data = load_qoe_req(args.qoe_file)[0]
            print("Sending QOE")
            r = requests.post("http://127.0.0.1:8001/go",data=qoe_data)
            HandlerClass = server_code.MakeHandlerClassFromArgv(sys.argv)
            try:
                time.sleep(6)
                l = [(400,4),(50,6),(400,6),(100,4),(1000,0)]
                play_scenar_list(l,qos)
                results = server_code.StoppableHttpServer.run_while_true(handler_class=HandlerClass)
                results["httpInfo"]=""
                pprint.pprint(results)
            except KeyboardInterrupt:
                print("Server interrupted")
                not_interrupted = False
                pass
            with open(RESULTS,"a") as f:
                line =\
                        line_out_of_dict(qos,qos_metrics)+','+\
                        line_out_of_dict(results,qoe_metrics)+"\n"
                f.write(line)
        except KeyboardInterrupt:
            not_interrupted=False
        #except Exception as e:
        #    print("Got one error : "+str(e))

def play_scenar_1(qos):
    """
    Functions for debugging. Will change the dl_rate
    during specific interval to get youtube stalling
    """
    time.sleep(2)
    qos['dl_rat_kb'] = 2800
    r = requests.post("http://127.0.0.1:8002/",data=qos)
    time.sleep(2)
    qos['dl_rat_kb'] = 100
    r = requests.post("http://127.0.0.1:8002/",data=qos)
    time.sleep(6)
    qos['dl_rat_kb'] = 3500
    time.sleep(4)
    r = requests.post("http://127.0.0.1:8002/",data=qos)
    qos['dl_rat_kb'] = 100
    r = requests.post("http://127.0.0.1:8002/",data=qos)
    time.sleep(2)

#Code to change the rate after a few seconds
#time.sleep(1)
#144p
#l = [(400,4),(50,6),(400,6),(100,4),(1000,0)]
#360p
#l = [(900,4),(50,6),(900,4),(100,2),(1000,0)]
#720p
#l = [(3000,3),(100,8),(3000,3),(100,8)]
#play_scenar_list(l,qos)
def play_scenar_list(l,qos):
    for (rate,sleep_time) in l:
        qos['dl_rat_kb'] = rate
        r = requests.post("http://127.0.0.1:8002/",data=qos)
        time.sleep(sleep_time)

if __name__== "__main__":
    main()
