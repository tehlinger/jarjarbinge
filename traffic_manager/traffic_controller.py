from subprocess import call
import time
from tc_commands import *
from pprint import pprint

class TrafficController:
    """
    Class responsible for modifying the traffic.
    """
    #A dummy interface must be setup for the incoming traffic
    inc_if_is_up = False
    net_conditions = {
            "ul_rat_kb":None,
            "dl_rat_kb":None,
            "ul_del_ms":None,
            "dl_del_ms":None,
            "ul_jit_ms":None,
            "dl_jit_ms":None,
            "ul_los":None,
            "dl_los":None}

    def set_rate(self,tp_kb,is_incoming,burst_kb=None,limit_kb=None):
        if not burst_kb:
            burst_kb = tp_kb
        if not limit_kb:
            limit_kb=burst_kb
        interface = self.in_if if is_incoming else self.out_if
        cmd = set_rate(interface,
                tp_kb,burst_kb,limit_kb)
        if call(cmd) != 0:
            raise OSError("Could not set rate to "+interface)

    def __init__(self,out_if="eth1",in_if="ifb0",ip="138.96.195.67/32"):
        self.out_if = out_if
        self.in_if = in_if
        self.ip = ip

    def set_conditions(self):
        if not TrafficController.inc_if_is_up:
            self.set_up_dummy_inc_interface()
        tc_cmds = to_cmd_list(TrafficController.net_conditions)
        for cmd in tc_cmds:
            if call(cmd) != 0:
                raise OSError("Couldn't use tc command:n"+cmd_to_string(cmd))
            else:
                print(cmd_to_string(cmd))
        return True

    def reset_all(self):
        cmd = clean_int_cmd(self.out_if)
        call(cmd)
        cmd = clean_int_cmd(self.in_if)
        call(cmd)
        TrafficController.net_conditions={
            "ul_rat_kb":None,
            "dl_rat_kb":None,
            "ul_del_ms":None,
            "dl_del_ms":None,
            "ul_jit_ms":None,
            "dl_jit_ms":None,
            "ul_los":None,
            "dl_los":None}


    def reset_if_redir(self):
    #Deletes the redirection to dummy ingress interface
        cmd = link_if_to_dummy_cmd(self.out_if,self.ip)
        cmd = revert_cmd(cmd)
        if call(cmd) != 0:
            raise OSError("Could not delete if redirection")
        TrafficController.inc_if_is_up = False
        return

    def set_up_dummy_inc_interface(self):
    #Sets the dummy interface for incoming traffic up.
        if not TrafficController.inc_if_is_up:
            if call(["modprobe","ifb"]) != 0:
                raise OSError("Could not load kernel module for dummy\
                        interface.")
            if call(["ip", "link", "set", "dev", self.in_if,"up"]) != 0:
                raise OSError("Could not set dummy interface up. Do you have the right to?")
            cmd = ["tc","qdisc","add","dev",self.out_if,"handle","ffff:",\
                    "ingress"]
            if call(cmd) != 0:
                print("Try setting handle ffff: for ingress eth0 :")
                #raise OSError(\
                #        "Could not set ingress handle interface :"+self.out_if)
            cmd = link_if_to_dummy_cmd(self.out_if,self.ip)
            if call(cmd) != 0:
                print(cmd_to_string(cmd))
                raise OSError(\
                        "Could not link dummy if to incoming interface :"+self.out_if)
            TrafficController.inc_if_is_up = True

def cmd_to_string(s):
    r = ""
    for i in s:
        r += i
        r += ' '
    return r

if __name__ == '__main__':
    t = TrafficController()
    try:
        d = t.net_conditions
        d['ul_del_ms']=500
        d['ul_jit_ms']=200
        d['ul_los_ms']=20
        t.net_conditions = d
        t.set_conditions()
        time.sleep(80)
    except Exception as e:
        print("Error : ")
        print(e)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt")
    finally:
        print("Try reset net_conditions")
        t.reset_all()
