import argparse
import pickle
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
from mos_p_1203 import get_itu_mos

HOST_NAME="127.0.0.1"
PORT_NUMBER = 8000
RESULTS = "results/grid_mos_1_B.csv"
qos_metrics = \
                ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms', 'ul_del_ms',
                        'dl_rat_kb', 'dl_jit_ms', 'ul_los']
qoe_metrics = \
['ITU_mos','QoE', 'availableQualityLevels', 'bufferSizeWhenStart', 'clen_audio',
'clen_video', 'dur', 'getVideoLoadedFraction', 'httpInfo', 'join_time',
'player_load_time', 'resolution', 'stallingNumber', 'timeout',
'totalStallDuration', 'ts_firstBuffering', 'ts_onPlayerReadyEvent',
'ts_onYTIframeAPIReady', 'ts_startPlaying', 'ts_start_js','video_id']

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
            qos = qos_selector.random_point()
            #Following are line to get a static qos conf
            #qos = QosSelector.get_clear_qos()
            #qos['dl_rat_kb'] = 8000
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
                #time.sleep(4)
                #l = [(100,9),(5750,3),(100,4),(4000,0)]
                #play_scenar_list(l,qos)
                results = server_code.StoppableHttpServer.run_while_true(handler_class=HandlerClass)
                results["httpInfo"]=""
                print("===RES===")
                pprint.pprint(results)
                print("===MOS===")
                if 'true_resolutions' not in results.keys():
                        print('Not launched')
                else:
                    try:
                        dic_for_mos = get_res_for_MOS(results)
                        if len(dic_for_mos['resolutions']) == 0:
                            print('Not launched.')
                        else:
                            mos = get_itu_mos(dic_for_mos)
                            pprint.pprint(mos)
                            results['ITU_mos'] = mos
                    except Exception as e:
                        print("Got one error : "+str(e))
                        mos = 0
                        results['ITU_mos'] = mos
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

def dump_resolutions_to_pck(results):
    test = get_res_for_MOS(results)
    with open("res_example.pck","wb") as test_file:
        pickle.dump(test,test_file)

def get_res_for_MOS(results):
    test = {}
    if 'stallingInfo' in results.keys():
        test['stalling'] = json.loads("["+results["stallingInfo"][0]+"]")
    else:
        test['stalling'] = []
    test['resolutions'] =\
            [i for i in\
            json.loads("["+str(results["true_resolutions"][0])+"]")\
            if '0x0' not in i['true_res']]

    test['video_id'] = results['video_id'][0]
    test['join_time'] = float(results['join_time'][0])
    test['end_time'] = float(results['end_time'][0])
    return test

if __name__== "__main__":
    main()
