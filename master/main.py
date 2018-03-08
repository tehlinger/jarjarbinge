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
from results_writer import *
from db_saver import *

HOST_NAME="127.0.0.1"
DB_IP = '138.96.65.33'
PORT_NUMBER = 8000
EXP_NAME = 'mongo_test_2'
RESULTS_FILE = "../results/"+EXP_NAME+".csv"

def main(fault_tolerant=False):
    """Launches experiment until Ctrl+C"""
    server_class = server_code.StoppableHttpServer
    not_interrupted = True
    while not_interrupted:
        try:
            launch_one_experiment()
        except KeyboardInterrupt:
            not_interrupted=False
        except Exception as e:
            if fault_tolerant:
                print("Got one error : "+str(e))
            else:
                raise e

def launch_one_experiment(verbose=True):
    qos = get_QoS(verbose=verbose)
    send_qos_to_traffic_controller(qos)
    send_go_to_qoe_measurer()
    results =\
            launch_local_server_and_wait_for_results(verbose=verbose,very_verbose=False)
    #write_results(results,qos,RESULTS_FILE)
    save_results(results,EXP_NAME,ip=DB_IP)

def write_results(results,qos,results_file):
    with open(results_file,"a") as f:
        line =\
                line_out_of_dict(qos,qos_metrics)+','+\
                line_out_of_dict(results,qoe_metrics)+"\n"
        f.write(line)

def launch_local_server_and_wait_for_results(verbose=True,very_verbose=False):
    HandlerClass = server_code.MakeHandlerClassFromArgv(sys.argv)
    try:
        results = server_code.StoppableHttpServer.run_while_true(handler_class=HandlerClass)
        results["httpInfo"]=""
        if verbose:
            if very_verbose:
                print("===RES===")
                pprint.pprint(results)
            print("===MOS===")
        if 'true_resolutions'  in results.keys():
            results = calc_MOS(results)
        else:
            if verbose:
                print('Not launched')
        return results
    except Exception as e:
        raise e

def send_go_to_qoe_measurer():
    r = requests.post("http://127.0.0.1:8001/go")

def send_qos_to_traffic_controller(qos,verbose=True):
    r = requests.post("http://127.0.0.1:8002/",data=qos)
    qos_response  = r.content.decode('utf-8')
    qos_response  = json.loads(r.content.decode('utf-8'))

def get_QoS(verbose=True,clear_qos_only=False):
    qos_selector = QosSelector(10)
    qos = qos_selector.random_point()
    #Following are line to get a static qos conf
    if clear_qos_only:
        qos = QosSelector.get_clear_qos()
    if verbose:
        print("=================================")
        print("QOS : ")
        pprint.pprint(qos)
    return qos

def calc_MOS(results):
    try:
        dic_for_mos = get_res_for_MOS(results)
        if len(dic_for_mos['resolutions']) == 0:
            print('Not launched.')
        else:
            mos = get_itu_mos(dic_for_mos,all_audio=True)
            pprint.pprint(mos)
            for codec, score in mos:
                cod_key = 'MOS_'+codec
                results[cod_key] = score
    except Exception as e:
        print("Got one error : "+str(e))
        mos = 0
        results['ITU_mos'] = mos
    return results

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

#def save_results(results):

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

