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
from subprocess import call

from qos_selector import *
from config_loader import *
from mos_p_1203 import get_itu_mos
from results_writer import *
from db_saver import *

P = 0.5

HOST_NAME="127.0.0.1"
#DB_IP = '138.96.65.33/acqua-db'
DB_IP = 'localhost'
PORT_NUMBER = 8000
EXP_NAME = 'v400r'
#EXP_NAME = 'useless'
RESULTS_FILE = "../results/"+EXP_NAME+".csv"
ALLWAYS_CLEAN_QOS=False
REALISTIC_DATA=True

def main(fault_tolerant=True):
    """Launches experiment until Ctrl+C"""
    server_class = server_code.StoppableHttpServer
    qos_selector = QosSelector()
    not_interrupted = True
    i = 0
    while not_interrupted:
        try:
            launch_one_experiment(qos_selector)
        except KeyboardInterrupt:
            not_interrupted=False
        except Exception as e:
            if fault_tolerant:
                print("Got one error : "+str(e))
            else:
                raise e

def launch_one_experiment(qos_selector,verbose=True):
    with_realistic_data = REALISTIC_DATA
    qos = get_QoS(qos_selector,with_realistic_data,verbose=verbose)
    send_qos_to_traffic_controller(qos)
    send_go_to_qoe_measurer()
    qoe_results =\
            launch_local_server_and_wait_for_results(verbose=verbose,very_verbose=False)
    send_clear_to_tc()
    try:
        save_results(qoe_results,qos,EXP_NAME,ip=DB_IP)
        #write_results(results,qos,RESULTS_FILE)
    except ValueError as e:
        raise e
    except Exception as e:
        pprint.pprint(e)
        try:
            save_results(qoe_results,qos,EXP_NAME,ip='localhost',must_format=False)
        except Exception as e:
            pprint.pprint(e)
            results = {**qos,**qoe_results}
            write_results(results,qos,RESULTS_FILE)
            raise e

def write_results(results,qos,results_file):
    with open(results_file,"a") as f:
        line =\
                line_out_of_dict(qos,qos_metrics)+','+\
                line_out_of_dict(results,qoe_metrics)+"\n"
        f.write(line)

def launch_local_server_and_wait_for_results(verbose=True,very_verbose=True):
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

def send_clear_to_tc():
    r = requests.post("http://127.0.0.1:8002/clear")
    qos_response  = r.content.decode('utf-8')
    qos_response  = json.loads(r.content.decode('utf-8'))

def get_QoS(qos_selector,realistic_data,verbose=True,clear_qos_only=ALLWAYS_CLEAN_QOS):
    if not realistic_data :
        qos = qos_selector.random_point(proba_clear_m=P)
    else:
        qos = qos_selector.random_real_point()
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
    except ValueError as e:
        raise e
    except Exception as e:
        print("Got one error : "+type(e)+" : "+str(e))
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

