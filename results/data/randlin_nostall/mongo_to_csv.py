import json

qos_metrics = \
                ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms', 'ul_del_ms',
                        'dl_rat_kb', 'dl_jit_ms', 'ul_los']

qoe_metrics = \
['MOS_mp2','MOS_ac3','MOS_aaclc','MOS_heaac','QoE', 'availableQualityLevels', 'bufferSizeWhenStart', 'clen_audio',
'clen_video', 'dur', 'getVideoLoadedFraction', 'httpInfo', 'join_time',
'player_load_time', 'resolution', 'stallingNumber', 'timeout',
'totalStallDuration', 'ts_firstBuffering', 'ts_onPlayerReadyEvent',
'ts_onYTIframeAPIReady', 'ts_startPlaying', 'ts_start_js','video_id']


with open("3B_clean_linrand.json","r") as f:
    cols =\
            qos_metrics+['MOS_mp2','MOS_ac3','MOS_aaclc','MOS_heaac','MOS']
    print(','.join(cols))
    for l in f:
        result = []
        d = json.loads(l)
        mos = 0
        for c in cols:
            if c in d.keys():
                if "MOS" in c:
                    mos += (d[c] * 0.25)
                result.append(d[c])
        if mos == 0:
            result += [0 for i in range(0,5)]
        else:
            result.append(mos)
        print(','.join([str(i) for i in result]))
