
qos_metrics = \
                ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms', 'ul_del_ms',
                        'dl_rat_kb', 'dl_jit_ms', 'ul_los']
qoe_metrics = \
['MOS_mp2','MOS_ac3','MOS_aaclc','MOS_heaac','QoE', 'availableQualityLevels', 'bufferSizeWhenStart', 'clen_audio',
'clen_video', 'dur', 'getVideoLoadedFraction', 'httpInfo', 'join_time',
'player_load_time', 'resolution', 'stallingNumber', 'timeout',
'totalStallDuration', 'ts_firstBuffering', 'ts_onPlayerReadyEvent',
'ts_onYTIframeAPIReady', 'ts_startPlaying', 'ts_start_js','video_id']

def header_line():
    r = ""
    for m in qos_metrics:
        r+= m + ","
    for m in qoe_metrics:
        r+= m + ","
    return r

def line_out_of_dict(d,keys):
    r = ""
    for k in keys:
        if k in d:
            value = d[k]
            if k == 'availableQualityLevels':
                r += ','
            else:
                if value == None:
                    value = ''
                else:
                    if type(value) is list and len(value) == 1\
                            and ',' not in value:
                        value = value[0]
                    try:
                        value  = float(value)
                    except:
                        value = value
                r += str(value)+','
        else:
            r += ","
    return r[:-1]

