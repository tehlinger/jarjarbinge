import random
import numpy as np
import pandas as pd
import itertools

class QosSelector:

    def get_clear_qos():
        return  {'dl_los': 0, 'dl_del_ms': 1, 'ul_rat_kb': None,\
                    'ul_jit_ms': None, 'ul_del_ms': 1, 'dl_rat_kb': None,\
                    'dl_jit_ms': None, 'ul_los': None}

    def __init__(self,pts_per_metric = 5):
        self.qos = \
                {'dl_los': None, 'dl_del_ms': None, 'ul_rat_kb': None,\
                'ul_jit_ms': None, 'ul_del_ms': None, 'dl_rat_kb': None,\
                'dl_jit_ms': None, 'ul_los': None}
        self.sup_inf = \
                {'dl_los': [0,21], 'dl_del_ms': [1,750],
                        'ul_rat_kb': [0,8000], 'ul_jit_ms': [0,300],
                    'ul_del_ms': [1,750], 'dl_rat_kb': [0,8000],
                        'dl_jit_ms': [0,300], 'ul_los': [0,21]}
        self.pts_per_metric = pts_per_metric
        self.points = self.generate_points()

    def simulate(self,n):
        l = [self.random_point() for i in range(0,n)]
        return pd.DataFrame(data=l)

    def generate_points(self):
        result = {}
        for metric, sup_inf in self.sup_inf.items():
            inf = sup_inf[0]
            sup = sup_inf[1]
            n = self.pts_per_metric
            result[metric] = \
                    [i for i in range(inf,sup,int((sup-inf)/n))]
        return result

    def random_point(self,proba_clear_m=0,N=8):
        result = {}
        n = 0
        for k, sup_inf in self.sup_inf.items():
            inf = sup_inf[0]
            sup = sup_inf[1]
            #value = random.randint(inf,sup)
            clear_metric = (random.random() < proba_clear_m)
            if 'kb' not in k:
                if clear_metric:
                    n += 1
                    value = inf
                else:
                    value = random.random() * (sup - inf)
            else:
                if clear_metric:
                    n += 1
                    value = sup
                else:
                    value = random.random() * (sup - inf)

            result[k] = round(int(value))
        result["n"] = n
        return result

    def get_list(self,p,n):
        return [self.random_point(p) for i in range(0,n)]

    def create_iterator(self):
        indexes = [list(range(0,self.pts_per_metric)) for i in range(0,8)]
        metrics = list(self.points.keys())
        #Builds every combination of the list of lists
        for pts_conf in itertools.product(*indexes):
            result = {}
            #print(pts_conf)
            for i in range(0,len(pts_conf)):
                pt = pts_conf[i]
                metric = metrics[i]
                value = self.points[metric][pt]
                if value == 0:
                    value = None
                result[metric] = value
            yield result

    def random_point_in_finite_space(self):
        indexes = [list(range(0,self.pts_per_metric)) for i in range(0,8)]
        metrics = list(self.points.keys())
        result = {}
        #print(pts_conf)
        for metric in metrics:
            value = self.points[metric]\
                    [random.randint(0,len(self.points[metric])-1)]
            if value == 0:
                value = None
            result[metric] = value
        return result



def get_qos():
    qos = \
            {'dl_los': None, 'dl_del_ms': None, 'ul_rat_kb': None,\
            'ul_jit_ms': None, 'ul_del_ms': None, 'dl_rat_kb': None,\
            'dl_jit_ms': None, 'ul_los': None}
    r1= random.randint(1,3)
    if r1== 1 :
        r1= 0
    if r1== 2:
        r1= random.randint(100,800)/100
    if r1== 3:
         r1= random.randint(900,3000)/100
    r = random.randint(1,3)
    if r == 1 :
        r = random.randint(10,800)
    if r == 2:
        r = random.randint(800,3000)
    if r == 3:
         r = random.randint(3000,30000)
    qos['ul_del_ms'] =1
    qos['ul_jit_ms'] = 2000
    #qos['dl_los'] = r1
    print("======")
    print("DL RATE "+str(qos['dl_rat_kb'])+"kbps")
    #print("LOSSES "+str(qos['dl_los'])+"%")
    return qos
