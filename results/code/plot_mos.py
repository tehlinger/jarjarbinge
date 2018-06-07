import array
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import numpy as np
import seaborn as sns
from numpy import reshape
import math
import datetime
import time

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

def mos_cdf(df,mos_field,legend,color="xkcd:sky blue",\
        title=None,ax=None,is_old=False):
    x = array.array('f',list(df[mos_field].sort_values()))
    y = [i/len(x) for i in range(1,len(x)+1)]
    if title is not None:
        if legend is None:
            lbl = get_bitrates(title)+"("+str(title)+")"
        else:
            lbl=legend
        style='ro' if is_old is True else 'D-'
        linestyle="--" if is_old else "-"
        ax.plot(x,y,linestyle=linestyle,label=lbl,color=color)
    else:
        linewidth=2 if is_old else 4
        linestyle="--" if is_old else "-"
        plt.plot(x,y,linestyle=linestyle,label=legend,color=color,\
                linewidth=linewidth)
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

def plot_all_mos(df,must_show,headers = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"],\
        legend=None,with_title=True,color="xkcd:sky blue",is_old=False):
    sns.set()
    n = df.shape[0]
    for h in headers:
        mos_cdf(df,h,legend,color,is_old=is_old)
    if with_title:
        plt.title("MOS for each codec ("+str(n)+" points, realistic dataset)",fontsize=22)
    plt.legend(numpoints=4,fontsize=22,markerscale=3)
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("MOS",fontsize=18)
    plt.ylabel("Distribution",fontsize=18)
    if must_show:
        plt.show()

def compare_MOS(a_df,b_df,df):
    headers = ["MOS"]
    plot_all_mos(a_df,False,["MOS"],legend="Wifi")
    plot_all_mos(b_df,False,["MOS"],legend="Mobile")
    plot_all_mos(df,False,["MOS"],legend="Both")
    n = a_df.shape[0]+b_df.shape[0]
    plt.title("MOS for each computer ("+str(n)+" points)",fontsize=22)
    plt.show()

def plot_acqua_mos(df,headers = ['yt_mos','skype_mos'],must_show=True):
    for mos in headers:
        l = df[mos].unique()
        #thanks stackoverflow :
        #https://stackoverflow.com/questions/14878538/duplicate-element-in-python-list?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        x = sorted([x for pair in zip(l,l) for x in pair])
        x = x[1:]+[5]
        l = [i/df.shape[0] for i in \
                list(df.groupby(mos).size().values)]
        y = sorted([x for pair in zip(l,l) for x in pair])
        plt.plot(x,y,label=mos)
    plt.legend()
    if must_show:
        plt.show()

def show_acqua_diff(is_log=True):
    df = pd.read_csv("../data/realistic_measures_with_acqua.csv")
    realistic_data['norm'] = realistic_data.apply(\
            lambda x : (((x.target-1.5)*4/3)+1),axis=1)
    plot_all_mos(realistic_data,False,\
            headers=['norm'],legend='Measured',with_title=False)
    plot_acqua_mos(realistic_data)
    plt.title('ACQUA predictd MOS versus measured MOS',fontsize=28)
    if is_log:
        plt.yscale('log')

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

def plt_mos_in_time_ab(dic):
    sns.set()
    plt_mos_in_time(dic['a'],"Computer A")
    plt_mos_in_time(dic['b'],"Computer B")
    plt.suptitle("Moving average of MOS (3 hours)",fontsize=20)
    formatter = FuncFormatter(currency)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.legend(fontsize=16)
    plt.xlabel("Time of the day",fontsize=18)
    plt.ylabel("MOS (moving average)",fontsize=18)
    plt.show()

def plt_ds_mos_in_time(ds):
    for ds_name, df in ds:
        plt_mos_in_time(df,ds_name,\
                from_d=datetime.datetime(2018,5,30,12),avg=1)
    plt.legend()
    plt.show()


def plt_mos_in_time(df,legend,from_d=datetime.datetime(2018,3,29,12),avg=20):
    df = df.loc[~pd.isnull(df.MOS)]
    df = df_with_datetimes(df)
    df = df.loc[df.date > from_d]
    X = df.date
    X = df.date.apply(lambda x :(x -datetime.datetime(1970,1,1)).total_seconds())
    Y = np.array(df.MOS)
    Y = moving_average(Y,avg)
    plt.plot(X,Y,label=legend)
    plt.xticks(np.arange(min(X), max(X)+1, 6*3600))

def currency(x, pos):
    return time.strftime('%H:%M', time.localtime(x))

def moving_average(a, n=3) :
    return np.convolve(np.array(list(a)), np.ones((n,))/n, mode='same')

def df_with_datetimes(df):
    result = df.copy()
    result["date"]=result.apply(lambda x : \
            datetime.datetime.strptime('2018/'+x.date,'%Y/%d/%m-%H:%M'),axis=1)
    return result


def plot_mixed_df_mos(df):
    datasets = list(df.dataset.unique())
    sns.set()
    colors = ["xkcd:bright blue","xkcd:neon green",\
            "xkcd:pale red","xkcd:silver",
            "xkcd:black","xkcd:warm grey"]
    for ds,c in zip(datasets,colors) :
        tmp_df = df.loc[df.dataset.str.match(ds)]
        plot_all_mos(tmp_df, False,headers=["MOS"],\
                legend=ds+\
                str(" ("+str(tmp_df.shape[0])+" pts)"),\
                with_title=False,color=c,is_old=False)
    plt.show()


def plot_all_datasets(ds_list,plt_title="MOS CDF for each dataset"):
    colors = ["xkcd:bright blue","xkcd:neon green",\
            "xkcd:pale red","xkcd:silver",
            "xkcd:black","xkcd:warm grey"]
    i = 0
    is_old=False
    for title,df in ds_list:
        c = colors[i]
        if i > 2:
            is_old=True
        plot_all_mos(df, False,\
                headers=["MOS"],legend=title[:10]+str(" ("+str(df.shape[0])+" pts)")\
                ,with_title=False,color=c,is_old=is_old)
        i += 1
    plt.title(plt_title,fontsize=28)
    plt.show()
