from codec_getter import codecGetter

def prepare_json_for_mos(play_dic,video_id="oFkulzWMotY"):
    stall_dic = get_stall_dic(play_dic)
    cg = codecGetter(video_id)
    vid_dic = merge_same_codec(get_vid_dic(play_dic,cg),is_video=True)
    aud_dic = merge_same_codec(get_aud_dic(play_dic,cg))
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
                formatted_seg_list(play_dic['resolutions'],end_time,codecs_getter,get_vid_seg)

def formatted_seg_list(seg_list,end_time,codecs_getter,get_codec_function):
    head = seg_list[0]
    start = round(head['ts'],4)
    end = round(get_next_ts(seg_list,end_time),4)
    seg = get_codec_function(head,codecs_getter)
    seg['dur'] = round(end - start,4)
    seg['start'] = start
    seg['res'] = head['true_res'].split('@')[0]
    if len(seg_list) == 1:
        return [seg]
    else:
        return [seg]+formatted_seg_list(seg_list[1:],end_time,codecs_getter,get_codec_function)

def merge_same_codec(seg_list,is_video=False,last_segment=None):
    """
    Ugly recursive function that takes one list of codecs
    and merges the same codecs in time.
    """
    head = seg_list[0]
    if len(seg_list) <= 1:
        if last_segment is None:
            return [head]
        else:
            if same_seg_type(last_segment,head,is_video):
                cumulated_seg = head.copy()
                cumulated_seg['start'] = last_segment['start']
                cumulated_seg['dur']   = head['dur']+last_segment['dur']
                return [cumulated_seg]
            else:
                return [last_segment]+[head]
    if last_segment is None or same_seg_type(last_segment,head,is_video):
        if is_video:
            print("i'm in")
        if last_segment is None:
            cumulated_seg = head.copy()
            cumulated_seg['start'] = head['start']
            cumulated_seg['dur']   = head['dur']
        else:
            cumulated_seg = head.copy()
            cumulated_seg['start'] = last_segment['start']
            cumulated_seg['dur']   = head['dur']+last_segment['dur']
        return merge_same_codec(seg_list[1:],is_video,cumulated_seg)
    else:
        return [last_segment]+merge_same_codec(seg_list[1:],is_video,head)

def same_seg_type(seg1,seg2,is_video):
    if is_video:
        return seg1['codec'] == seg2['codec'] and\
                seg1['bitrate'] == seg2['bitrate'] and\
                seg1['res'] == seg2['res']
    else:
        return seg1['codec'] == seg2['codec'] and\
                seg1['bitrate'] == seg2['bitrate']

def get_aud_dic(play_dic,codecs_getter):
    if len(play_dic['resolutions']) == 0:
        return None
    else:
        end_time = play_dic['end_time']
        play_dic['resolutions'][0]['ts'] = 0
        return\
                formatted_seg_list(play_dic['resolutions'],\
                end_time,codecs_getter,get_aud_seg)

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

def get_aud_seg(s,codecs_getter):
    vid_codec_id = s['codecs'][1]
    return codecs_getter.get(int(vid_codec_id))
