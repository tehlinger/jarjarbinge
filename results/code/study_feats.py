import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from math import ceil
from numpy import corrcoef

def analyze(df,prev_field="est_last",new_metric="est_first"):
    df = add_prev_rate_to_df(df,prev_field)
    colors = ["b","g","r"]
    for ds_name,c in zip(df.dataset.unique(),colors):
        tmp_df = df.loc[df.dataset.str.match(ds_name)]
        plot_dependency(tmp_df,new_metric,c)
    plt.xlabel("Previous rate")
    plt.ylabel(new_metric.replace("_"," ").capitalize())
    plt.legend()
    plt.xlim([100,1e4])
    plt.ylim([100,1e4])
    #plt.xscale('log')
    #plt.loglog()
    plt.show()

def add_prev_rate_to_df(df,field):
    result = df.copy()
    result = result.reset_index()
    prev_rates = result[field].values[:-1]
    n = result.shape[0]
    result = result.drop([0])
    result["prev_rate"] = prev_rates
    return result

def plot_dependency(df,new_metric,color="k"):
    dataset = list(df.dataset.unique())[0]
    df = df.loc[(df.est_first > 100) & (df.prev_rate > 100)]
    y = df[new_metric]
    x = df.prev_rate
    print(dataset+" : "+str(corrcoef(x,y)[0][1]))
    sns.set()
    #sns.regplot("prev_rate",new_metric,data=df,fit_reg=True)
    plt.scatter(x,y,color=color,label=dataset)

def find_same_qos_points(df):
    qos_metrics = ['dl_los', 'dl_del_ms',\
            'ul_rat_kb', 'ul_jit_ms', 'ul_del_ms',\
            'dl_rat_kb', 'dl_jit_ms', 'ul_los', 'RTT']
    to_watch=qos_metrics+['dataset']
    return df.duplicated(subset=to_watch,keep=False)

def bin_metric(df,metric,bin_size):
    df["bins"] = df.apply(lambda x : round(x[metric]/bin_size)*bin_size,axis=1)
    return df

def get_n_per_bin(df,metric,bin_size):
    tmp_df = bin_metric(df,metric,bin_size)
    return \
            tmp_df[["bins","join_time"]].groupby("bins").size().reset_index()

def plot_bin(df,metric_to_bin,bin_size,metric_to_plot,min_size=5):
    tmp_df = get_bin_info(df,metric_to_bin,bin_size,min_size)
    grouped_df = tmp_df[["bins",metric_to_plot]].groupby("bins").describe().reset_index()
    x = grouped_df.bins
    y1 = grouped_df[metric_to_plot]["mean"]
    ymin = grouped_df[metric_to_plot]["min"]
    ymax = grouped_df[metric_to_plot]["max"]
    ymin2 = grouped_df[metric_to_plot]["25%"]
    ymax2 = grouped_df[metric_to_plot]["75%"]
    sns.set()
    plt.plot(x,y1,marker='o',linestyle="--",c="xkcd:dark green")
    plt.plot(x,ymin,color="xkcd:faded green")
    plt.plot(x,ymax,color="xkcd:faded green")
    plt.fill_between(x,ymin,ymax,interpolate=True,color="xkcd:hospital green")
    plt.fill_between(x,ymin2,ymax2,interpolate=True,color="xkcd:medium green")
    plt.ylabel("MOS",fontsize=28)
    plt.xlabel("First connection speed",fontsize=28)
    plt.suptitle("Average MOS per first connection speed (at least "+\
            str(min_size)+" measure per bin)",fontsize=30)
    plt.show()

def get_bin_info(df,metric,bin_size,min_n_per_bin):
    bins=bin_metric(df,metric,bin_size)
    bin_sizes=get_n_per_bin(df,metric,bin_size)
    df_with_bin_size=bins.merge(bin_sizes,on="bins",how="left")
    df_with_bin_size["bin_size"]=df_with_bin_size[0]
    df_with_bin_size.drop(columns=[0],inplace=True)
    return df_with_bin_size.loc[df_with_bin_size["bin_size"] >= min_n_per_bin]
