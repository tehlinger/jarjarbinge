LINK_D_ID_TO_ETH = ["tc", "filter", "add", "dev", "eth1", "parent",
        "ffff:", "u32", "match", "ip", "dst","138.96.195.167/32",
       "action", "mirred", "egress", "redirect", "dev", "ifb0"]

def link_if_to_dummy_cmd(eth_id,ip=None):
    """
    Returns the formatted command to link ifb dummy command
    to the interface passed as argument
    """
    result = LINK_D_ID_TO_ETH.copy()
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

def set_rate(interface, tp_kb,burst_kb,limit_kb):
    CMD_LIST = \
            ["sudo", "tc", "qdisc", "add", "dev", interface, "root", "handle",
                    "1:", "tbf", "rate", str(tp_kb)+"kbit", "burst",
            str(burst_kb)+"kbit", "limit", str(limit_kb)+"kbit"]
    return CMD_LIST

def clean_int_cmd(interface):
    CMD_LIST = ["tc", "qdisc", "del", "dev", interface, "root"]
    return CMD_LIST

def root_handle_cmd(interface):
    return ["tc", "qdisc", "add", "dev", interface, "root", "handle", "1:"]

def child_handle_cmd(interface):
    return ["tc", "qdisc", "add", "dev", interface, "parent", "1:1","handle", "10:"]

def netem_cmd(interface,is_up,net_cond):
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
                dl_cmd += [str(jit)+"ms","distribution","normal"]
            result += dl_cmd
        if los:
            los_cmd = ["loss", str(los)+"%"]
            result += los_cmd
        return result
    else:
        raise Exception('net_cond has no delay or loss to implement')

def has_netem(net_cond,is_up):
    if is_up:
            return (net_cond["ul_del_ms"] != None or
            net_cond["ul_los"] != None)
    else:
        return (net_cond["dl_del_ms"] != None or
            net_cond["dl_los"] != None)
