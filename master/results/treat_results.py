import pprint
from matplotlib.lines import Line2D
import math
from matplotlib import colors as mcolors
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_summary(measures_file:'str'='grid_random_beta.csv'):
    df = pd.read_csv(measures_file)
    return df

def compare_pcs(file_1 = "beta_shit.csv",file_2 = "beta_finite.csv"):
   shit_df = pd.read_csv(file_1)
   good_df = pd.read_csv(file_2)
   comp_df = \
           pd.merge(good_df,shit_df,how='outer',on=\
           ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms',
               'ul_del_ms','dl_rat_kb', 'dl_jit_ms', 'ul_los'],\
                       suffixes=('_good','_bad'))
   same_mes_df = \
           comp_df[~np.isnan(comp_df.QoE_bad) & ~np.isnan(comp_df.QoE_good)]
   print("Same measures : "+str(same_mes_df.shape[0]))
   print_dif(same_mes_df,'QoE_bad','QoE_good')
   print_dif(same_mes_df,'join_time_bad','join_time_good')


def print_dif(merged_df,field1,field2):
   same_results = merged_df[merged_df[field1] == merged_df[field2]].shape[0]
   diff_results = merged_df[merged_df[field1] != merged_df[field2]].shape[0]
   print("Different"+str(field1.split('_')[:-1])+"  : "+str(diff_results)+" on " +str(same_results))

class Summary:

    color_dic = { 'hd1080' : 'green',
                  'hd720'  : 'lightgreen',
                  'large'  : 'yellow',
                  'medium' : 'orange',
                  'small'  : 'red',
                  'tiny'   : 'firebrick',
                  'dead'   : 'black'}
    #MANICHEAN GRID OF COLOR
    #color_list =\
    #        ['red','red','red','red','red',
    #        'green','green','green','green','green']

    #NON-MANICHEAN GRID
    color_list =\
            ['black','black','red','red',
            'orange','orange','yellow',
            'yellow','green','green']
    #color_list = ['black', 'grey', 'sienna', 'firebrick', 'red', 'orange',
    #'greenyellow','yellow', 'lightgreen', 'forestgreen','green']


    qos_metrics = ['dl_los', 'dl_del_ms', 'ul_rat_kb', 'ul_jit_ms',
               'ul_del_ms','dl_rat_kb', 'dl_jit_ms', 'ul_los']

    def __init__(self,measures_file:'str'='grid_random_beta.csv'):
        self.df = pd.read_csv(measures_file)
        self.df = self.df.fillna(0)
        self.nb_played = self.df[self.df.join_time < 300000].resolution.size
        self.df.loc[(self.df.join_time > 300000) \
                | ((self.df.ts_startPlaying == 0)
                & (self.df.resolution == "hd1080"))\
                ,'resolution']= "dead"

    def __len__(self):
        return self.df.shape[0]

    def __str__(self):
        return "Played : " +str(self.nb_played)+"/"+str(len(self))

    def show_grid(self,res=None):
        if res != None:
            df = self.df[self.df.resolution == res]
        else:
            df = self.df
        cols = list(set(Summary.qos_metrics+["resolution"])\
                -set(['ul_rat_kb','ul_jit_ms','dl_jit_ms']))
        g = sns.PairGrid(df[cols])
        g.map_upper(plt.scatter)
        g.add_legend()
        plt.show()

    def simple_scat(self,x='dl_del_ms',y='dl_rat_kb'):
        #sns.lmplot(data=self.df,x='dl_rat_kb',y='dl_del_ms',hue='resolution',
        #        fit_reg=False)
        g = sns.FacetGrid(self.df, col='resolution',hue='resolution')
        g = g.map(plt.scatter, x="dl_del_ms",y  ='dl_rat_kb')
        plt.show()

    def med_scat(self,x_metric,y_metric,ax):
        df = med_res_df(self.df,x_metric,y_metric)
        for res in df.resolution.unique():
            if res != 0:
                #c = Summary.color_dic[res]
                c = 'k'
                x = list(df[df.resolution == res][x_metric])
                y = list(df[df.resolution == res][y_metric])
                ax.scatter(x,y,color=c)
                ax.set(xlabel=x_metric,ylabel=y_metric)

    def prop_scat(self,x_metric,y_metric,ax,min_meas):
        df = proportion_res_df(self.df,x_metric,y_metric,min_meas)
        for color in df[0].unique():
            if color != 0:
                #c = Summary.color_dic[res]
                x = list(df[df[0] == color][x_metric])
                y = list(df[df[0] == color][y_metric])
                ax.scatter(x,y,color=mcolors.CSS4_COLORS[color],s=80)
                ax.set(xlabel=x_metric,ylabel=y_metric)

    def nice_grid(self,min_meas=0):
        cols = list(set(Summary.qos_metrics+["resolution"])\
                -set(['ul_rat_kb','ul_jit_ms','dl_jit_ms','resolution']))
        width = len(cols)
        fig, axes = plt.subplots(width-1,width-1)
        for m1 in cols:
            for m2 in cols:
                if m1 != m2:
                    x = cols.index(m1)
                    y = cols.index(m2)
                    if x > y:
                        ax = axes[y][x-1]
                        self.prop_scat(m1,m2,ax,min_meas)
                        #ax.set(xlabel=x,ylabel=y)
        #plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
        #                        wspace=None, hspace=None)
        blank_space = 0.20
        plt.subplots_adjust(hspace=0.57,wspace=blank_space)
        custom_legend(axes[2][1])
        #plt.tight_layout()
        plt.show()

def custom_legend(ax):
    custom_lines = [\
            Line2D([0], [0], color=mcolors.CSS4_COLORS['black'], lw=4),\
            Line2D([0], [0], color=mcolors.CSS4_COLORS['red'], lw=4),\
            Line2D([0], [0], color=mcolors.CSS4_COLORS['orange'], lw=4),\
            Line2D([0], [0], color=mcolors.CSS4_COLORS['yellow'], lw=4),\
            Line2D([0], [0], color=mcolors.CSS4_COLORS['green'], lw=4)]
    ax.legend(custom_lines, \
            ['<20 %', '<40 %', '<60 %','<80 %','<100 %'],
            loc='center',title='Percentage of videos that could play :')

def proportion_res_df(df,col1,col2,min_meas):
    """
    For a measures dataframe, gathers all the points having the same
    value for col1 and col2 and applies a color depending on the pro-
    portion of measures with resolution 'dead'.
    """
    #df = df.loc[df.resolution != 'dead']
    result = df[[col1,col2,'resolution']].groupby([col1,col2]).apply(
                    lambda x : x[x['resolution'] != 'dead'].shape[0]/ \
                            x.shape[0])\
                            .dropna().apply(\
                            lambda x : Summary.color_list[math.floor(x * 10)])\
                            .reset_index()
    result['nb_meas'] = df[[col1,col2,'resolution']].groupby([col1,col2]).apply(
                    lambda x : x.shape[0])\
                            .values
    return result[result['nb_meas'] > min_meas]

def med_res_df(df,col1,col2):
    #df = df.loc[df.resolution != 'dead']
    return \
            df[[col1,col2,'resolution']].dropna().groupby([col1,col2]).apply(
                    pd.DataFrame.mode).reset_index(drop=True)
    #return \
    #        df[[col1,col2,'resolution']].groupby([col1,col2]).apply(
    #                lambda x : x[x['resolution'] != 'dead'
    #                    ].shape[0]).dropna().reset_index(drop=True)
