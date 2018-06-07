def get_link_cmd():
    return  ["tc", "filter", "add", "dev", None, "parent",
            "ffff:", "u32", "match", "ip", "dst","138.96.195.67/32",
            "action", "mirred", "egress", "redirect", "dev", "ifb0"]


def link_if_to_dummy_cmd(eth_id,ip=None):
    """
    Returns the formatted command to link ifb dummy command
    to the interface passed as argument
    """
    result = get_link_cmd()
    result[4] = eth_id
    if ip :
        result[11]=ip
    return result

def revert_cmd(cmd):
    """
    Takes a command and replaces add with del
    """
    i = cmd.index("add")
    result = cmd.copy()
    result[i] = "del"
    i = cmd.index("ffff:") + 1
    return result[:i]

def set_rate(interface, tp_kb,burst_kb,limit_kb,latency):
    CMD_LIST = \
            ["sudo", "tc", "qdisc", "add", "dev", interface, "root", "handle",
                    "1:", "tbf", "rate", str(tp_kb)+"kbit", "burst",
            str(burst_kb)+"kbit", "limit", str(latency)+"ms"]
    return CMD_LIST

def clean_int_cmd(interface):
    CMD_LIST = ["tc", "qdisc", "del", "dev", interface, "root"]
    return CMD_LIST

def to_cmd_list(net_cond,out_if,in_if):
    """
    For a given net_cond dict (example of dict after), returns
    the list of tc commands needed to setup the conditions.
    If rate must be changed -> one command ('tbf')
    If delay and/or jit and/or jit  must be changed -> one command ('netem')
    Once for upload, and once for download.

    Net_cond dictionnary :
    {'ul_rat_kb': None, 'dl_rat_kb': None, 'ul_del_ms': None, 'dl_del_ms':
    None, 'ul_jit_ms': None, 'dl_jit_ms': None, 'ul_los': None, 'dl_los': None}
    """
    cmd_list = []
    has_up = is_up(net_cond)
    has_down = is_down(net_cond)
    if (not has_up) and (not has_down):
        raise Exception('No command to extract from netcond : \n'+str(net_cond))
    if has_up:
        if has_tbf(net_cond,True):
            cmd_list += [root_handle_cmd(out_if) + tbf_cmd(True,net_cond)]
            if has_netem(net_cond,True):
                cmd_list +=\
                        [child_handle_cmd(out_if)+netem_cmd(True,net_cond)]
        else:
            cmd_list += \
                    [root_handle_cmd(out_if)+netem_cmd(True,net_cond)]
    if has_down:
        if has_tbf(net_cond,False):
            cmd_list += \
                    [root_handle_cmd(in_if)+tbf_cmd(False,net_cond)]
            if has_netem(net_cond,False):
                cmd_list +=\
                        [child_handle_cmd(in_if)+netem_cmd(False,net_cond)]
        else:
                cmd_list +=\
                        [root_handle_cmd(in_if)+netem_cmd(False,net_cond)]
    return cmd_list

def root_handle_cmd(interface):
    return ["tc", "qdisc", "add", "dev", interface, "root", "handle", "1:"]

def child_handle_cmd(interface):
    return ["tc", "qdisc", "add", "dev", interface, "parent", "1:1","handle", "10:"]

def netem_cmd(is_up,net_cond):
    """
    Must be combined with the beginning of the cmd
    which is given by either 'child_handle_cmd' or
    'root_handle_cmd'
    """
    if has_netem(net_cond,is_up):
        result = ["netem"]
        if is_up:
            dl  = net_cond["ul_del_ms"]
            jit = net_cond["ul_jit_ms"]
            los = net_cond["ul_los"]
        else:
            dl  = net_cond["dl_del_ms"]
            jit = net_cond["dl_jit_ms"]
            los = net_cond["dl_los"]
        if dl:
            dl_cmd = ["delay",str(dl)+"ms"]
            if jit:
                dl_cmd += [str(jit)+"ms",\
                        "distribution","normal","rate","100mbit"]
            result += dl_cmd
        if los:
            los_cmd = ["loss", str(los)+"%"]
            result += los_cmd
        return result
    else:
        raise Exception('net_cond has no delay or loss to implement')

def tbf_cmd(is_up,net_cond):
    """
    Must be combined with the beginning of the cmd
    which is given by either 'child_handle_cmd' or
    'root_handle_cmd'
    """
    if has_tbf(net_cond,is_up):
        result = ["tbf"]
        if is_up:
            rate  = net_cond["ul_rat_kb"]
            latency = net_cond["ul_del_ms"]
        else:
            rate  = net_cond["dl_rat_kb"]
            latency = net_cond["dl_del_ms"]
        return result +\
                ["rate",str(rate)+"kbit","burst","50kbit","latency",str(latency)+"ms"]
    else:
        raise Exception('net_cond has no throuhput to implement')

def has_netem(net_cond,is_up):
    if is_up:
            return (net_cond["ul_del_ms"] != None or
            net_cond["ul_los"] != None)
    else:
        return (net_cond["dl_del_ms"] != None or
            net_cond["dl_los"] != None)

def has_tbf(net_cond,is_up):
    if is_up:
        return net_cond["ul_rat_kb"] != None
    else:
        return net_cond["dl_rat_kb"] != None

def is_up(net_cond):
        return (net_cond["ul_rat_kb"] != None or
                net_cond["ul_del_ms"] != None or
                net_cond["ul_jit_ms"] != None or
                net_cond["ul_los"] != None)

def is_down(net_cond):
        return (net_cond["dl_rat_kb"] != None or
                net_cond["dl_del_ms"] != None or
                net_cond["dl_jit_ms"] != None or
                net_cond["dl_los"] != None)
