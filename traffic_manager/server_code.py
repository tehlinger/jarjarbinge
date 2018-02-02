from http.server import BaseHTTPRequestHandler,HTTPServer
import time
from urllib import parse
import pprint

from traffic_controller import TrafficController

def page_write(self,message):
    self.wfile.write(message.encode('utf-8'))

def MakeHandlerClassFromArgv(init_args):
    """
    Returns the class (class factory)
    Allows  to add instances var to the class
    """
    class QoSHandler(BaseHTTPRequestHandler):

        tc = None

        def __init__(self,*args, **kwargs):
            super(QoSHandler, self).__init__(*args, **kwargs)

        def _set_headers(self):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                #if path=="/results":

        def do_POST(self):
            """Response do a POST"""
            if QoSHandler.tc == None:
               QoSHandler.tc = TrafficController()
            QoSHandler.tc.reset_all()
            received_net_cond = self.get_net_conditions()
            #pprint.pprint(received_net_cond)
            TrafficController.net_conditions = received_net_cond
            #The network conditions of the machine are chenged HERE
            QoSHandler.tc.set_conditions()
            self.send_response(200)
            self.send_header("Content-type","application/json")
            self.end_headers()
            self.wfile.write('{"qos":"READY"}'.encode("utf-8"))
            print("Conditions set : "+\
                    str(TrafficController.net_conditions['dl_rat_kb'])+"kbps, "+
                    str(TrafficController.net_conditions['dl_los'])+"%")


        def get_net_conditions(self):
            """Converts all the values of the param_dict to floats"""
            cond_dict = self.get_params().copy()
            for k in cond_dict.keys():
                if 'rat' in k:
                    cond_dict[k] = int(cond_dict[k][0])
                else:
                    cond_dict[k] = float(cond_dict[k][0])
            return cond_dict

        def get_params(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            qos_params = parse.parse_qs(post_data.decode('utf-8'))
            return qos_params

    return QoSHandler
