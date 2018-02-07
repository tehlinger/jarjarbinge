import pprint

FILE = "beta.csv"

with open(FILE,"r") as f:
    result = {}
    for l in f.readlines():
        k = len(l.split(','))
        if k in result :
            result[k] +=1
        else:
            result[k] = 1
    pprint.pprint(result)

