import pandas as pd
import datetime

def print_now():
    print(datetime.datetime.now())

def cook():
    realistic_data = pd.read_csv("../../../ml/data/realistic.csv")
    acqua_data = pd.read_csv("realistic_source.csv")
    acqua_data.RTT = pd.to_numeric(acqua_data.RTT,errors='coerce')
    acqua_data = acqua_data.loc[~pd.isnull(acqua_data.RTT)]
    acqua_data = acqua_data.loc[acqua_data.RTT < 1e100]
    acqua_data.RTT       = acqua_data.apply(lambda x : x.RTT/1e6,axis=1)
    acqua_data.ul_rat_kb = acqua_data.apply(lambda x : x.ul_rat_kb/1e3,axis=1)
    acqua_data.dl_rat_kb = acqua_data.apply(lambda x : x.dl_rat_kb/1e3,axis=1)
    acqua_data.dl_jit_ms = acqua_data.apply(lambda x : x.dl_jit_ms/1e6,axis=1)
    acqua_data.ul_jit_ms = acqua_data.apply(lambda x : x.ul_jit_ms/1e6,axis=1)
    return (acqua_data,realistic_data)

def find_match(x,acqua_data):
    matches = acqua_data.loc[
            (round(x.ul_del_ms + x.dl_del_ms) == round(acqua_data.RTT)) &
            (round(x.ul_jit_ms) == round(acqua_data.ul_jit_ms)) &
            (round(x.ul_jit_ms) == round(acqua_data.ul_jit_ms)) &
            (round(x.ul_rat_kb) == round(acqua_data.ul_rat_kb)) &
            (round(x.dl_rat_kb) == round(acqua_data.dl_rat_kb))
            ]
    if matches.shape[0] == 0 :
        return pd.Series((0,0))
    else:
        return pd.Series((matches.iloc[0].yt_mos,matches.iloc[0].skype_mos))
        #return pd.Series((matches.shape[0],matches.shape[0]))

#acqua_data, realistic_data=cook()
