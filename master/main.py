import argparse
import json
import time
import pprint
import requests
import urllib3
import server_code

from config_loader import *

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('qoe_file',help="Filepath to qoe_configs")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                                action="store_true")
    args = parser.parse_args()
    return args

TEST_QOS = \
        {'dl_los': None, 'dl_del_ms': 100, 'ul_rat_kb': None,\
        'ul_jit_ms': None, 'ul_del_ms': None, 'dl_rat_kb': 300,\
        'dl_jit_ms': None, 'ul_los': None}

def main():
    not_interrupted = True
    args = get_args()
    verbose = args.verbose
    if verbose:
        print("QoE conf loaded.")
    data = load_qoe_req(args.qoe_file)
    while not_interrupted:
        try:
            for d in data:
                #r = requests.post("http://127.0.0.1:8001/",data=d)
                r = requests.post("http://127.0.0.1:8002/",data=TEST_QOS)
                if verbose:
                    print(r.status_code,r.reason)
                qos_response  = r.content.decode('utf-8')
                pprint.pprint(qos_response)
                qos_response  = json.loads(r.content.decode('utf-8'))
                if qos_response['qos'] == 'READY':
                    print('QOS set.')
                    pprint.pprint(TEST_QOS)
                time.sleep(60)
        except KeyboardInterrupt:
            if verbose:
                print("Interrupted")
            not_interrupted=False
        except (requests.exceptions.ConnectionError,ConnectionRefusedError):
            if verbose:
                print("Unable to connect to QoE measurer. Retry in 2sec.")
        time.sleep(30)

if __name__== "__main__":
    main()
