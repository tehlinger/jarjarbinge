from subprocess import call
import static_commands

class TrafficController:
    """
    Class responsible for modifying the traffic.
    """

    #A dummy interface must be setup for the incoming traffic
    inc_if_is_up = False

    def set_rate(tp_kb,is_incoming,burst_kb=None,limit_kb=None):
        if not burst_kb:
            burst_kb = tp_kb
        if not limit_kb:
            limit_kb=burst_kb

    def __init__(self,in_if="eth1",ip="138.96.195.67/32"):
        self.in_if = in_if
        self.ip = ip

    def reset_if_redir(self):
    #Deletes the redirection to dummy ingress interface
        cmd = static_commands.link_if_to_dummy_cmd(self.in_if,self.ip)
        cmd = static_commands.revert_cmd(cmd)
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
            if call(["ip", "link", "set", "dev", "ifb0","up"]) != 0:
                raise OSError("Could not set dummy interface up. Do you have the right to?")
            cmd = static_commands.link_if_to_dummy_cmd(self.in_if,self.ip)
            if call(cmd) != 0:
                raise OSError(\
                        "Could not link dummy if to incoming interface :"+self.in_if)
            TrafficController.inc_if_is_up = True

def cmd_to_string(s):
    r = ""
    for i in s:
        r += i
        r += ' '
    return r
