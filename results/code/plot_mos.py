import pandas as pd
import numpy as np
import seaborn as sns

def mos_cdf(df):
    x = array.array('f',list(df.MOS.sort_values()))
    y = [i/len(x) for i in range(1,len(x)+1)]
    plt.plot(x,y)

def by_vid_mos(df,split_vids=True):
    if split_vids:
        for vid_id in [i for i in list(df.vid_id.unique()) if type(i) == str]:
            mos_cdf(df.loc[df.vid_id == vid_id])
    else:
        mos_cdf(df)
    plt.title("CDF of the MOS",fontsize=22)
    plt.show()
