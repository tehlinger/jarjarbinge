import pprint
import pandas as pd
import numpy as np

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
