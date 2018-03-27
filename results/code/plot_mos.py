import array
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from numpy import reshape
import math

ids = [
    "bUhdSs0VK9c",
    "im_2tkN4VKY",
    "O3zza3ofZ0Q",
    "oFkulzWMotY",
    "RSzD92Rl8j4",
    "tSjhLFWj9TU"
    ]


def get_bitrates(v_id):
    df = pd.read_csv(open("../../dash_manifests/"+v_id+".csv"))
    df = df.loc[df.web_format == "mp4"]
    return "-".join(list(df.bitrate)[-3:])

def mos_cdf(df,mos_field,legend,title=None,ax=None):
    x = array.array('f',list(df[mos_field].sort_values()))
    y = [i/len(x) for i in range(1,len(x)+1)]
    if title is not None:
        if legend is None:
            lbl = get_bitrates(title)+"("+str(title)+")"
        else:
            lbl=legend
        ax.plot(x,y,label=legend)
    else:
        plt.plot(x,y,label=legend)
    #sns.kdeplot(df[mos_field],label=mos_field.split('_')[1])

def by_vid_mos(df,mos_field="MOS",split_vids=True):
    if split_vids:
        fig,ax = plt.subplots()
        for vid_id in [i for i in list(df.vid_id.unique()) if type(i) == str]:
            mos_cdf(df.loc[df.vid_id == vid_id],mos_field,vid_id,ax)
        handles, labels = ax.get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t:
            t[0]))
        ax.legend(handles,labels,fontsize=20)
        plt.title("CDF of the MOS of each video",fontsize=20)
        plt.xlabel("MOS",fontsize=20)
        plt.ylabel("CDF",fontsize=20)
    else:
        mos_cdf(df,mos_field)

def plot_all_mos(df,headers = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"],\
        legend=None):
    sns.set()
    n = df.shape[0]
    for h in headers:
        mos_cdf(df,h,legend)
    #plt.title("MOS for each codec ("+str(n)+" points)",fontsize=22)
    plt.legend(fontsize=18)
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("MOS",fontsize=18)
    plt.ylabel("Distribution",fontsize=18)
    #plt.show()

def compare_MOS(a_df,b_df,df):
    headers = ["MOS"]
    plot_all_mos(a_df,["MOS"],legend="computer A")
    plot_all_mos(b_df,["MOS"],legend="computer B")
    plot_all_mos(df,["MOS"],legend="Both")
    n = a_df.shape[0]+b_df.shape[0]
    plt.title("MOS for each computer ("+str(n)+" points)",fontsize=22)
    plt.show()

def violins(df):
    qos_metrics = \
                    ['dl_los', 'ul_los', 'dl_del_ms', 'ul_del_ms',
                        'dl_rat_kb','ul_rat_kb','dl_jit_ms', 'ul_jit_ms']
    met_dic = {
            "del":"delay (ms)",
            "jit":"jitter (ms)",
            "rat":"throughput (Kbps)",
            "los":"loss rate (%)"}
    fig, axs = plt.subplots(4,2)
    axs = np.array(axs)
    for m in qos_metrics:
        direction = "Download" if m[0] == 'd' else "Upload"
        title = direction + " " +met_dic[m.split('_')[1]]
        i = qos_metrics.index(m)
        ax = axs.reshape(-1)[i]
        sns.violinplot(data=df,x=m,y="MOS",ax=ax);
        ax.set_xlabel(title,fontsize=16)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95,
            wspace=0.05, hspace=0.3)
    plt.suptitle("Distribution of the MOS for each point in each metric",
            fontsize=20)
    plt.show()

