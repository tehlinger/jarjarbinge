import pandas as pd
import math

V1_RESULT_FILES = [
                "../data/2A_clean_linrand.json",
                "../data/2B_clean_linrand.json",
                "../data/3B_clean_linrand.json",
                "../data/3A_clean_linrand.json",
                "../data/4B_clean_linrand.json",
                "../data/4A_clean_linrand.json"
                ]

V2_RESULT_FILES = [
        #"../data/v2/Av2_0_clean.json",
        #"../data/v2/Bv2_0_clean.json",
        #"../data/v2/Av2_2_clean.json",
        #"../data/v2/Av2_2_clean.json",
        #"../data/v2/Av2_3_clean.json",
        #"../data/v2/Bv2_3_clean.json",
        "../data/v2/biais_A_v2_4_clean.json",
        "../data/v2/biais_A_v2_41_clean.json",
        "../data/v2/biais_A_v2_42_clean.json",
        #"../data/v2/biais_B_v2_4_clean.json",
        #"../data/v2/biais_B_v2_41_clean.json",
        #"../data/v2/biais_B_v2_42_clean.json",
        "../data/v2/v300b_A_clean.json",
        #"../data/v2/v300b_B_clean.json",
        "../data/v2/v310b_A_clean.json",
        #"../data/v2/v310b_B_clean.json"
        ]

REALIST_RESULTS = [
        "../data/v2/v400r_A_clean.json"
        ]

MOS_HEADERS = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]

def load_col_names(f):
    with open(f,'r') as f :
        return f.readline()[:-1].split(',')

def compare_pcs(filenames=V2_RESULT_FILES):
    """
    indexes : indexes of the filenames of each computer
    """
    a_files = [f for f in filenames if "A" in f]
    a_df = load_csv(False,a_files)
    add_mean_mos(a_df)
    b_files = [f for f in filenames if "B" in f]
    b_df = load_csv(False,b_files)
    add_mean_mos(b_df)
    return {"a":a_df,"b":b_df}

def check_files():
    for f in V2_RESULT_FILES:
        df = pd.read_json(f,lines=True)
        df = launched_vid(df)
        add_mean_mos(df)
        df = df.loc[~pd.isnull(df.MOS)]
        a = df.MOS
        t = st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a))
        t = ("{0:.2f}".format(t[0]),"{0:.2f}".format(t[1]))
        print(f.split('/')[-1].split('.')[0][-12:]\
                +":"+"n="+str(len(a)).zfill(4)+" i="+str(t))

def load_results(files,header_file : 'file_path' =
        '../data/header.txt'):
    is_csv = "csv" in files[0]
    df = load_csv(is_csv,files,header_file)
    df = fill_nans(df)
    return df

def load_csv(is_csv,files=V1_RESULT_FILES,\
        header_file='../data/header.txt'):
    columns = load_col_names(header_file)
    result = None
    for fp in files:
        if is_csv:
            df = pd.read_csv(fp,names=columns)
        else:
            df = pd.read_json(fp,lines=True)
        if result is not None:
            result = result.append(df)
        else:
            result = df
        print("File : "+str(fp)+"-"+str(df.shape)+" entries.")
    return result

def export_for_ml(df,output):
    cols = df.columns
    excluded = [i for i in df.columns if "MOS_" in i]+["date"]
    out_cols = list(set(cols) - set(excluded))
    df.to_csv(output,columns=out_cols,index=False)


def load_MOS(files=V2_RESULT_FILES,header_file : 'file_path' = '../data/header_mos.txt'):
    df = load_triple_MOS(files,header_file)
    add_mean_mos(df)
    df.loc[df.join_time == 310000,"MOS"] = 1
    df.loc[df.player_load_time == 310000,"MOS"] = 1
    df.at[pd.isnull(df.true_resolutions),"true_resolutions"] = None
    return df

def load_triple_MOS(files,header_file : 'file_path' =
        '../data/header.txt'):
    df = load_results(files,header_file)
    for mos in ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]:
        df.loc[df.join_time == 310000,mos] = 1
        df.loc[df.player_load_time == 310000,mos] = 1
    return df

def add_mean_mos(df):
    mos_headers = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]
    df['MOS'] = df.apply(lambda x : sum([\
            x[i]*0.25 for i in mos_headers]),axis=1)

def fill_nans(df):
    col_with_nans = get_labels_with_NaNs(df)
    for c in col_with_nans:
        if 'dl_' in c or 'ul_' in c:
            df[c] = df[c].fillna(0)
    return df

def get_labels_with_NaNs(df):
    d = df.isna().any()
    return list(d.loc[d].index)
