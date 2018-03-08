import pandas as pd

RESULT_FILES = ["../data/grid_mos_1_A.csv",
                "../data/grid_mos_1_B.csv"]

MOS_HEADERS = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]

def load_col_names(f):
    with open(f,'r') as f :
        return f.readline()[:-1].split(',')

def load_results(files : 'str_list'=RESULT_FILES,header_file : 'file_path' = '../data/header.txt'):
    df = load_csv(files,header_file)
    fill_nans(df)
    return df

def load_csv(files : 'str_list'=RESULT_FILES,header_file : 'file_path' = '../data/header.txt'):
    columns = load_col_names(header_file)
    result = None
    for fp in files:
        df = pd.read_csv(fp,names=columns)
        if result is not None:
            result = result.append(df)
        else:
            result = df
    return result

def load_MOS(files : 'str_list'=RESULT_FILES,header_file : 'file_path' =
        '../data/header_mos.txt'):
    df = load_results(files,header_file)
    df.loc[df.join_time == 310000,"MOS"] = 1
    df.loc[df.player_load_time == 310000,"MOS"] = 1
    return df

def load_triple_MOS(files : 'str_list'=RESULT_FILES,header_file : 'file_path' =
        '../data/header.txt'):
    df = load_results(files,header_file)
    for mos in ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]:
        df.loc[df.join_time == 310000,mos] = 1
        df.loc[df.player_load_time == 310000,mos] = 1
    return df

def fill_nans(df):
    col_with_nans = get_labels_with_NaNs(df)
    for c in col_with_nans:
        if 'dl_' in c or 'ul_' in c:
            df[c] = df[c].fillna(0)
    return df

def get_labels_with_NaNs(df):
    d = df.isna().any()
    return list(d.loc[d].index)
