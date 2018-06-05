import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from load_data import NEW_DATASET,OLD_DATASET

def plot_mos_depending_on(dataset,metric,condition_function):
    sns.set()
    good_dataset = dataset.loc[condition_function(dataset)]
    bad_dataset = dataset.loc[~condition_function(dataset)]

    size=good_dataset.shape[0]
    x  = good_dataset[metric]
    y  = good_dataset["MOS"]
    sns.regplot(x,y,color="g")

    size=bad_dataset.shape[0]
    x  = bad_dataset[metric]
    y  = bad_dataset["MOS"]
    sns.regplot(x,y,color="r")

def metric_in_row_lower_than(row,metric,t):
    return row[metric] < t
