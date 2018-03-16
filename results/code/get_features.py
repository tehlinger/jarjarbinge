import pandas as pd

from load_data import load_results


def meas_per_mos(df):
    if "MOS" not in df.columns:
        add_mean_mos(df)
    df["category"] = df.MOS.apply(lambda x : 0 if pd.isnull(x) else math.floor(x))
    return df[["video_id","category"]].groupby("category").count()
