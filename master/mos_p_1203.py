from codec_getter import codecGetter

def prepare_json_for_mos(play_dic,video_id="oFkulzWMotY"):
    stall_dic = get_stall_dic(play_dic)
    cg = codecGetter(video_id)
    vid_dic = get_vid_dic(play_dic,cg)
    aud_dic = get_aud_dic(play_dic,cg)
    return {
            "IGen" : static_gen_entry(),
            "I11"  : aud_dic,
            "I13"  : vid_dic,
            "I23"  : stall_dic
            }


def static_gen_entry():
    return {
            "displaySize":"640x390",
            "device":"pc",
            "viewingDistance":None
            }


def get_stall_dic(play_dic):
    result = get_join_time(play_dic)
    for d in play_dic['stalling']:
        result.append([float(d['ts']),float(d['duration'])/1000])
    return result

def get_join_time(play_dic):
    """Extracts and format the 'join_time' entry of the dic"""
    if ('join_time' in d.keys()) and d['join_time'] is not None\
            and d['join_time'] > 0:
                return [[0,float(d['join_time'])/1000.0]]
    else:
        return []

def get_vid_dic(play_dic,codecs_getter):
    if len(play_dic['resolutions']) == 0:
        return None
    else:
        end_time = play_dic['end_time']
        play_dic['resolutions'][0]['ts'] = 0
        return\
                formatted_seg_list(play_dic['resolutions'],end_time,codecs_getter)


def formatted_seg_list(seg_list,end_time,codecs_getter):
    head = seg_list[0]
    start = head['ts']
    end = get_next_ts(seg_list,end_time)
    seg = get_vid_seg(head,codecs_getter)
    seg['dur'] = end - start
    seg['start'] = start
    if len(seg_list) == 1:
        return [seg]
    else:
        return [seg]+formatted_seg_list(seg_list[1:],end_time,codecs_getter)

def get_next_ts(seg_list,end_time):
    if len(seg_list) > 1:
        return seg_list[1]['ts']
    else :
        return end_time


def is_first_seg(seg_list):
    return len(seg_list) == 0

def get_vid_seg(s,codecs_getter):
    vid_codec_id = s['codecs'][0]
    return codecs_getter.get(int(vid_codec_id))

def get_aud_dic(play_dic,codecs_getter):
    raise NotImplementedError()
