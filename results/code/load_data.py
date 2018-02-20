import pandas as pd

RESULT_FILES = ["../data/B_grid_random_beta_B.csv",
                "../data/grid_random_beta.csv"]



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

def fill_nans(df):
    col_with_nans = get_labels_with_NaNs(df)
    for c in col_with_nans:
        if 'dl_' in c or 'ul_' in c:
            df[c] = df[c].fillna(0)
    return df

def get_labels_with_NaNs(df):
    d = df.isna().any()
    return list(d.loc[d].index)
