import json
import pprint

def load_qoe_req(f):
    with open(f,"r") as fd:
        return json.load(fd)
