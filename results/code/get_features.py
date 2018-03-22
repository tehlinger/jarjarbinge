import pandas as pd
import numpy as np

from load_data import load_results


def meas_per_mos(df):
    if "MOS" not in df.columns:
        add_mean_mos(df)
    df["category"] = df.MOS.apply(lambda x : 0 if pd.isnull(x) else math.floor(x))
    return df[["video_id","category"]].groupby("category").count()

def loaded_players_only(df):
    return df.loc[df.player_load_time < 310000]

def launched_vid(df):
    df = loaded_players_only(df)
    return df.loc[df.join_time < 310000]

def add_app_features(df):
    #stalling
    add_stalling_feat(df)
    #Res
    df = add_res_features(df)
    return df

def add_stalling_feat(df):
    df[["stall_tot","stall_n","stall_max"]] = \
            df.apply(extract_stall_info,axis=1)

def add_res_feat(df):
    df[["switches_nb","switches_freq","res_min",\
            "res_max","res_mod"]] = \
            df.apply(extract_res_info,axis=1)

def extract_stall_info(stall_dic):
    """
    Given a stallingInfo dic, returns
    <T (total length),n,max> length
    """
    if not isinstance(stall_dic,list):
        return pd.Series((0,0,0))
    else:
        return pd.Series((sum([(i['duration']/1000) for i in stall_dic]),
                len(stall_dic), max([(i['duration']/1000) for i in stall_dic])))

def extract_res_info(entry):
    """Given an entry, returns
    <nb_switches,frequency>
    """
    if entry['true_resolutions'] is None:
        return pd.Series((0,0,0,0,0))
    else:
        of_interest = [i for i in entry['true_resolutions']\
                if '0x0' not in i['true_res']]
        switches_nb = len(of_interest)
        switches_freq = switches_nb/entry['end_time']
        res_list = get_res_list(of_interest,entry['end_time'])
        res_min = min([i[0] for i in res_list])
        res_max = max([i[0] for i in res_list])
        res_mod = max(res_list,key= lambda x : x[1])[0]
        return pd.Series((switches_nb,switches_freq,\
                res_min,res_max,res_mod))

def get_res_list(of_interest,end_time):
    """
    For a resolution dict, returns
    a list of [(<res>,<dur>)]
    that gives the list of resolutions the video
    was played on for duration <dur>
    """
    result = {}
    previous_ts = 0
    for dic in [i for i in of_interest if '0x0' not in i['true_res']]:
        res = get_yt_res(dic["true_res"])
        dur = dic["ts"]-previous_ts
        previous_ts = dic["ts"]
        result.setdefault(res,0)
        result[res] += dur
        last_res = res
    result[last_res] += (end_time - previous_ts)
    return [i for i in result.items()]

def get_yt_res(yt_str):
    """
    For a given sting like '1280x720@30'
    returns 720 (for 720p)
    """
    return int(yt_str.split('x')[1].split('@')[0])
