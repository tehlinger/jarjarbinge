import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

def plot_random_est_rates(df,n_samples,width=3):
    sns.set()
    df = df.loc[(~pd.isnull(df.est_rates))]
    df = df.loc[df.dl_rat_kb < 8000]
    df['len'] = df.est_rates.apply(lambda x : len(x))
    df = df.loc[df.len > 20]
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
