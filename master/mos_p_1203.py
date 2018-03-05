from codec_getter import codecGetter
import itu_p1203
import pickle

def get_itu_mos(results,all_audio=False):
    """
    Get the O.46 itu-t MOS (std P.1203
    If all_audio is true, returns the score for every possible
    audio codec.
    """
    input_dic = prepare_json_for_mos(results,results["video_id"])
    if not all_audio:
        return itu_p1203.P1203Standalone(input_dic).calculate_complete()['O46']
    else:
        result = []
        for audio_codec in ["mp2", "ac3", "aaclc", "heaac"]:
            set_aud_codec(input_dic,audio_codec)
            result.append((audio_codec,itu_p1203.P1203Standalone(input_dic).calculate_complete()['O46']))
        return result


def set_aud_codec(input_dic,audio_codec):
   for aud_seg in input_dic["I11"]["segments"]:
       aud_seg["codec"] = audio_codec


def prepare_json_for_mos(play_dic,video_id,audio_codec=None):
    stall_dic = get_stall_dic(play_dic)
    cg = codecGetter(video_id)
    vid_dic = merge_same_codec(get_vid_dic(play_dic,cg),is_video=True)
    aud_dic = merge_same_codec(get_aud_dic(play_dic,cg))
    return {
            "IGen" : static_gen_entry(),
            "I11"  : {
                "streamId" : 42,
                "segments" : aud_dic
                },
            "I13"  : {
                "streamId" : 42,
                "segments" : vid_dic,
                },
            "I23"  : {
                "streamId" : 42,
                "stalling" : stall_dic
                }
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
    if ('join_time' in play_dic.keys()) and play_dic['join_time'] is not None\
            and play_dic['join_time'] > 0:
                return [[0,float(play_dic['join_time'])/1000.0]]
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
    seg['duration'] = round(end - start,4)
    seg['start'] = start
    seg['resolution'] = head['true_res'].split('@')[0]
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
                cumulated_seg['duration']= head['duration']+last_segment['duration']
                return [cumulated_seg]
            else:
                return [last_segment]+[head]
    if last_segment is None or same_seg_type(last_segment,head,is_video):
        if last_segment is None:
            cumulated_seg = head.copy()
            cumulated_seg['start'] = head['start']
            cumulated_seg['duration']   = head['duration']
        else:
            cumulated_seg = head.copy()
            cumulated_seg['start'] = last_segment['start']
            cumulated_seg['duration'] = head['duration']+last_segment['duration']
        return merge_same_codec(seg_list[1:],is_video,cumulated_seg)
    else:
        return [last_segment]+merge_same_codec(seg_list[1:],is_video,head)

def same_seg_type(seg1,seg2,is_video):
    if is_video:
        return seg1['codec'] == seg2['codec'] and\
                seg1['bitrate'] == seg2['bitrate'] and\
                seg1['resolution'] == seg2['resolution']
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
