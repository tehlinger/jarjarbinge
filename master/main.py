import argparse
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
RESULTS = "results/useless.csv"

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
    qos_iterator = QosSelector(2).create_iterator()
    while not_interrupted:
        try:
            for qos in qos_iterator :
                print("QOS : ")
                pprint.pprint(qos)
                r = requests.post("http://127.0.0.1:8002/",data=qos)
                print("Sent QoS request")
                qos_response  = r.content.decode('utf-8')
                pprint.pprint(qos_response)
                qos_response  = json.loads(r.content.decode('utf-8'))
                if qos_response['qos'] == 'READY':
                    print('QOS set.')
                qoe_data = load_qoe_req(args.qoe_file)[0]
                print("Sending QOE")
                r = requests.post("http://127.0.0.1:8001/go",data=qoe_data)
                HandlerClass = server_code.MakeHandlerClassFromArgv(sys.argv)
                try:
                    #Code to change the rate after a few seconds
                    #time.sleep(5)
                    #qos['dl_rat_kb'] = 1000
                    #r = requests.post("http://127.0.0.1:8002/",data=qos)
                    results = server_code.StoppableHttpServer.run_while_true(handler_class=HandlerClass)
                except KeyboardInterrupt:
                    print("Server interrupted")
                    not_interrupted = False
                    pass
                with open(RESULTS,"a") as f:
                    if qos != None:
                        f.write(
                                str(qos['dl_los'])+\
                                ","+str((qos['dl_rat_kb']))+\
                                #","+str(int(results['join_time'][0]))+\
                                #","+str(int(results['QoE'][0]))+\
                                #","+str(float(results['bufferSizeWhenStart'][0]))+\
                                #","+str(float(results['getVideoLoadedFraction'][0]))+\
                                #","+str(float(results['stallingNumber'][0]))+\
                                "\n")
                results["httpInfo"]=""
                pprint.pprint(results)
        except KeyboardInterrupt:
            not_interrupted=False

if __name__== "__main__":
    main()
