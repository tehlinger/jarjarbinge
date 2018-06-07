import pandas as pd
import numpy as np
import math

from load_data import load_results

qos_metrics = ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms',
           'ul_del_ms','dl_rat_kb', 'dl_jit_ms', 'ul_los','RTT']

def build_binary_dataset(df):
    """
    Returns a DF with qos_metrics only and a
    target variable "LAUNCHED" which is true if the
    video launched
    """
    result = df.copy()
    result["LAUNCHED"] = \
            result.apply(lambda x : (x["player_load_time"] < 3e5) and\
            (x["join_time"] < 3e5) ,axis=1)
    l = qos_metrics + ["LAUNCHED"]
    return result[l]

def add_feats_to_ds(ds):
    result = {}
    for ds_name, df in ds:
        result[ds_name] = get_feats_for_ml_only(df)
    return result

def get_feats_for_ml_only(df,\
        exclude_qos=False,excluded_cols=[],with_est_rate=True,\
        add_dummies=False):
    df = launched_vid(df)
    df = add_RTT(df)
    to_exclude = set(qos_metrics) if exclude_qos else set()
    excluded_cols = set(excluded_cols)
    res = df[list(set(df.columns)-to_exclude\
            -set(["date","video_id","n","dur","_id"])
            -excluded_cols
            -set(["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]))]
    res = add_app_features(res)
    if with_est_rate:
        res = add_est_rate_feat(res)
    res = res.loc[~pd.isnull(res.MOS)]
    res = with_categorized_res(res)
    if add_dummies:
       res = one_col_per_res(res)
       res = res.drop(columns=\
               [i for i in res.columns if 'res' in i and \
               len(i.split('_')) == 2])
    return\
            res[list(set(res.columns)\
            -set(['true_resolutions','totalStallDuration','stallingInfo',\
            "getVideoLoadedFraction",\
            "est_rates"\
            ]))]

def one_col_per_res(df):
    #res_dic = {0:'0',1:'144',2:'240',3:'360',4:'480',5:'720',6:'1080'}
    res_cols = [i for i in df.columns if 'res_' in i]
    return pd.get_dummies(df,columns=res_cols)

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

def with_categorized_res(df,columns=["res_min","res_max","res_mod"]):
    dic = {0:0,144:1,240:2,360:3,480:4,720:5,1080:6}
    result = df.copy()
    for c in columns:
        result[c] = result.apply(lambda x : dic[int(x[c])],axis=1)
    return result

def add_RTT(df):
    result = df.copy()
    result["RTT"] = \
            result.apply(\
            lambda x : x.dl_del_ms + x.ul_del_ms,axis=1)
    return result

def add_app_features(df):
    if launched_vid(df).shape[0] < df.shape[0]:
        raise  ValueError(\
                "Dataframe has entries that are videos that didn't play (perhaps use launched_vid(df) first?")
    #stalling
    df = add_stalling_feat(df)
    #Res
    df = add_res_feat(df)
    return df

def add_est_rate_feat(df):
    result = df.copy()
    result[["est_rate_max","est_rate_min","est_rat_med",\
            "est_rate_integral","est_first","est_last"]] =\
            df.est_rates.apply(extract_est_rates_info)
    result["available_integral"] = \
            result.apply(lambda x : x.dl_rat_kb * x.end_time,axis=1)
    result["left_int"] = result.apply(\
            lambda x :  x.available_integral - x.est_rate_integral,\
            axis=1)
    result["rat_needed"] = result.apply(\
            lambda x : x["est_rate_integral"]/x["end_time"],axis=1)
    return result

def add_stalling_feat(df):
    result = df.copy()
    result[["stall_tot","stall_n","stall_max","stall_last_ts"]] = \
            df.stallingInfo.apply(extract_stall_info)
    return result

def add_res_feat(df):
    result = df.copy()
    result[["switches_nb","switches_freq","res_min",\
            "res_max","res_mod","res_first","res_last_ts",\
            "res_last","forlast_res","forlast_res_ts"]] = \
            df.apply(extract_res_info,axis=1)
    return result

def extract_est_rates_info(est_rate_dic):
    """
    Given a stallingInfo dic, returns
    <T (total length),n,max> length
    """
    if not isinstance(est_rate_dic,list):
        return pd.Series((0))
    else:
        values=[i["res"] for i in est_rate_dic]
        first = values[0]
        last = values[-1]
        integral = integrate_est_rates(est_rate_dic)
        return pd.Series((max(values),min(values),np.median(values),\
                integral,first,last))

def extract_stall_info(stall_dic):
    """
    Given a stallingInfo dic, returns
    <T (total length),n,max> length
    """
    if not isinstance(stall_dic,list):
        return pd.Series((0,0,0))
    else:
        return pd.Series((sum([(i['duration']/1000) for i in stall_dic]),
                len(stall_dic), max([(i['duration']/1000) for i in stall_dic]),\
                        stall_dic[-1]['ts']))

def extract_res_info(entry):
    """Given an entry, returns
    <nb_switches,frequency>
    """
    if entry['true_resolutions'] is None \
            or isinstance(entry['true_resolutions'],str):
        return pd.Series((0,0,0,0,0))
    else:
        of_interest = [i for i in entry['true_resolutions']\
                if '0x0' not in i['true_res']]
        switches_nb = len(of_interest)
        if entry['end_time'] > 0:
            switches_freq = switches_nb/entry['end_time']
        else:
            switches_freq = 0
        res_list = get_res_list(of_interest,entry['end_time'])
        if len(res_list) > 0:
            res_min = min([i[0] for i in res_list])
            res_max = max([i[0] for i in res_list])
            res_first = res_list[0][0]
            res_mod = max(res_list,key= lambda x : x[1])[0]
            last_change_ts = res_list[-1][1]
            last_res = res_list[-1][0]
            if len(res_list) > 1:
                forlast_res = res_list[-2][0]
                forlast_res_ts = res_list[-2][1]
            else:
                forlast_res = res_first
                forlast_res_ts = 0
        else:
            res_min = 0
            res_max = 0
            res_mod = 0
            last_change_ts = 0
            last_res = "0x0"
            forlast_res = "0x0"
            forlast_res_ts = 0
        return pd.Series((switches_nb,switches_freq,\
            res_min,res_max,res_mod,res_first,last_change_ts,\
            last_res,forlast_res,forlast_res_ts))

def get_res_list(of_interest,end_time):
    """
    For a resolution dict, returns
    a list of [(<res>,<dur>)]
    that gives the list of resolutions the video
    was played on for duration <dur>
    """
    result = {}
    previous_ts = 0
    last_res = None
    for dic in [i for i in of_interest if '0x0' not in i['true_res']]:
        res = get_yt_res(dic["true_res"])
        dur = dic["ts"]-previous_ts
        previous_ts = dic["ts"]
        result.setdefault(res,0)
        result[res] += dur
        last_res = res
    if last_res is not None:
        result[last_res] += (end_time - previous_ts)
    return [i for i in result.items()]

def get_yt_res(yt_str):
    """
    For a given sting like '1280x720@30'
    returns 720 (for 720p)
    """
    return int(yt_str.split('x')[1].split('@')[0])

def integrate_est_rates(res_dic):
    l = [(i["res"],i["ts"]) for i in res_dic]
    prev_time = 0
    sum_rate = 0
    for(res,ts) in l:
        delta = ts - prev_time
        sum_rate += delta * res
        prev_time = ts
    return sum_rate

def show_res_ts():
    df = get_feats_for_ml_only(load_MOS(["../data/new_jitter/test.json"]))
    return df[["res_last_ts","res_last","forlast_res","forlast_res_ts"]]
