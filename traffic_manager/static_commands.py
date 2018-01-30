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
