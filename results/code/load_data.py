import pandas as pd
import math
import all_ds

def BIG_SCREEN():
    return load_MOS(all_ds.BIG_2)

def BIG_SCREEN_DEPENDANT():
    return load_MOS(all_ds.BIG_1)

def OLD_DATASET():
    return [
        ("Old realistic",load_MOS(all_ds.REALISTIC)),
        ("Old random",load_MOS(all_ds.FULL_RANDOM)),
        ("Old normalized",load_MOS(all_ds.V2_RESULT_FILES))
        ]

def NEW_DATASET():
    return [
        ("New E",load_MOS(all_ds.V3_REAL)),
        ("New N",load_MOS(all_ds.V3_NORM)),
        ("New FR",load_MOS(all_ds.V3_FR))
        ]

def DATASET_WRONG_QUEUE():
    return [
        ("R  WQ",load_MOS(all_ds.V0_REAL)),
        ("N  WQ",load_MOS(all_ds.V0_NORM)),
        ("FR WQ",load_MOS(all_ds.V0_FR))
        ]

def merge_all_ds(ds):
    #supposes this order of experiments :
    #full_random -> normalized -> realistic
    result = None
    n = None
    for ds_name, dataset in ds:
        if "FR " in ds_name :
            n = 10
        else:
            if "R " in ds_name:
                n = 59
            if "N" in ds_name :
                n = 30
        dataset = add_seconds_to_ds(n,dataset)
        dataset["ds"] = ds_name
        print(dataset.iloc[0].ds)
        if result is None:
            result = dataset
        else:
            result = result.append(dataset,ignore_index=True)
    return result.sort_values("date").reset_index()

def add_seconds_to_ds(n,df):
    result = df.copy()
    if n < 10 :
        s = "0"+str(n)
    else:
        s = str(n)
    result["date"] = result.apply(lambda x : x["date"]+":"+s,axis=1)
    return result


def load_col_names(f):
    with open(f,'r') as f :
        return f.readline()[:-1].split(',')

def compare_pcs(filenames):
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

def load_csv(is_csv,files,\
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


def load_MOS(files_list,header_file='../data/header_mos.txt'):
    df = load_triple_MOS(files_list,header_file)
    add_mean_mos(df)
    df.loc[df.join_time == 310000,"MOS"] = 1
    df.loc[df.player_load_time == 310000,"MOS"] = 1
    if "true_resolutions" in df.columns:
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
    if 'MOS' not in df.columns:
        mos_headers = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]
        df['MOS'] = df.apply(lambda x : sum([\
                x[i]*0.25 for i in mos_headers]),axis=1)
    else:
        if 'target' in df.columns:
            df['MOS'] = df.target

def fill_nans(df):
    col_with_nans = get_labels_with_NaNs(df)
    for c in col_with_nans:
        if 'dl_' in c or 'ul_' in c:
            df[c] = df[c].fillna(0)
    return df

def get_labels_with_NaNs(df):
    d = df.isna().any()
    return list(d.loc[d].index)
