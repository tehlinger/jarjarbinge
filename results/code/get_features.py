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
    #BR switches
    df = add_br_features(df)
    #Res
    df = add_res_features(df)
    return df

def add_stalling_feat(df):
    df[["stall_tot","stall_n","stall_max"]] = \
            df.apply(extract_stall_info,axis=1)

def add_br_features(df):
    pass

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

def extract_br_info(entry):
    """Given an entry, returns
    <nb_switches,frequency>
    """
    if entry['true_resolutions'] is None:
        return (0,0)
    else:
        of_interest = [i for i in entry['true_resolutions']\
                if '0x0' not in i['true_res']]
        return len(of_interest)

def add_res_features(df):
    pass
