import pandas as pd

V1_RESULT_FILES = [
                "../data/2A_clean_linrand.json",
                "../data/2B_clean_linrand.json",
                "../data/3B_clean_linrand.json",
                "../data/3A_clean_linrand.json",
                "../data/4B_clean_linrand.json",
                "../data/4A_clean_linrand.json"
                ]

V2_RESULT_FILES = [
        "../data/v2/Av2_0_clean.json",
        "../data/v2/Bv2_0_clean.json",
        "../data/v2/Av2_2_clean.json",
        "../data/v2/Bv2_2_clean.json"
        ]

MOS_HEADERS = ["MOS_mp2","MOS_ac3","MOS_aaclc","MOS_heaac"]

def load_col_names(f):
    with open(f,'r') as f :
        return f.readline()[:-1].split(',')

def load_results(files : 'str_list'=V2_RESULT_FILES,header_file : 'file_path' =
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
    return result

def load_MOS(files : 'str_list'=V2_RESULT_FILES,header_file : 'file_path' =
        '../data/header_mos.txt'):
    df = load_triple_MOS(files,header_file)
    add_mean_mos(df)
    df.loc[df.join_time == 310000,"MOS"] = 1
    df.loc[df.player_load_time == 310000,"MOS"] = 1
    df.at[pd.isnull(df.true_resolutions),"true_resolutions"] = None
    return df

def load_triple_MOS(files : 'str_list'=V2_RESULT_FILES,header_file : 'file_path' =
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
