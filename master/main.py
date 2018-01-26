import argparse
import pprint
import requests

from config_loader import *

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('qoe_file',help="Filepath to qoe_configs")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                                action="store_true")
    args = parser.parse_args()
    return args

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
                r = requests.post("http://127.0.0.1:8000/",data=d)
                if verbose:
                    print(r.status_code,r.reason)
        except KeyboardInterrupt:
            if verbose:
                print("Interrupted")
            not_interrupted=False

if __name__== "__main__":
    main()
