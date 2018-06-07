import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

from load_data import load_MOS
from get_features import get_feats_for_ml_only,launched_vid

def plot_mos_depending_on(feats_df,metric_1,metric_2=None):
    if metric_2 is None:
        metric_2 = "MOS"
    df = feats_df.copy()
    df = df.sort_values(metric_2).reset_index()
    x = df[metric_1]
    y = df[metric_2]
    sns.set()
    plt.xlim([0,10000])
    plt.scatter(x,y)
    plt.show()

def get_data_for_feat_plots(with_est_rate=True):
    df = launched_vid(load_MOS())
    if with_est_rate:
        df = df.loc[~pd.isnull(df.est_rates)]
    return get_feats_for_ml_only(df,\
            with_est_rate=with_est_rate)

def plot_scatter(x,y,df,style=None):
    sns.set()
    if style is None:
        sns.jointplot(df[x],df[y])
    else:
        sns.jointplot(df[x],df[y],style)
    plt.show()

def plot_random_est_rates(df,n_samples,width=3):
    if "est_rate_max" not in df.columns:
        raise ValueError("Est_rates features not in df."+\
                "Try using add_app_features(df) or "+\
                "add_app_features(df)")
    sns.set()
    df = df.loc[(~pd.isnull(df.est_rat_med))]
    df = df.loc[(df.stall_n) >1 & (df.stall_tot > 10)]
    samples = df.sample(n_samples)
    print(samples.shape)
    n_rows = math.ceil(n_samples/width)
    fig,axs = plt.subplots(n_rows,width)
    for i in range(0,samples.shape[0]):
        sample = samples.iloc[i]
        est_rates = sample.est_rates
        ax = axs.reshape(-1)[i]
        y = [i["res"] for i in est_rates]
        x = [i["ts"] for i in est_rates]
        ax.axhline(y=sample.dl_rat_kb, color='b',linestyle='--', linewidth=1)
        ax.plot(x,y)
    plt.show()
