import numpy as np
import pandas as pd

def count_outliers(df, Q1, Q3, IQR, columns):
    cut_off = IQR * 1.5
    temp_df = (df[columns] < (Q1 - cut_off)) | (df[columns] > (Q3 + cut_off))
    return [len(temp_df[temp_df[col]]) for col in temp_df]

def calc_skew(df, columns=None):
    if columns is None:
        columns = df.columns
    return [df[col].skew() for col in columns]

def percentage(lst):
    return [str(round(((value / 150001) * 100), 2)) + '%' for value in lst]

def remove_outliers(df, columns):
    for col in columns:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        cut_off = IQR * 1.5
        lower, upper = Q1 - cut_off, Q3 + cut_off
        df = df.drop(df[df[col] > upper].index)
        df = df.drop(df[df[col] < lower].index)
    return df

def replace_outliers_with_fences(df, columns):
    for col in columns:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        cut_off = IQR * 1.5
        lower, upper = Q1 - cut_off, Q3 + cut_off
        df[col] = np.where(df[col] > upper, upper, df[col])
        df[col] = np.where(df[col] < lower, lower, df[col])
    return df

def getOverview(df, columns) -> pd.DataFrame:
    min_val = df[columns].min()
    Q1_val = df[columns].quantile(0.25)
    median_val = df[columns].quantile(0.5)
    Q3_val = df[columns].quantile(0.75)
    max_val = df[columns].max()
    IQR_val = Q3_val - Q1_val
    skew_val = calc_skew(df, columns)
    outliers_val = count_outliers(df, Q1_val, Q3_val, IQR_val, columns)
    cut_off_val = IQR_val * 1.5
    lower_val, upper_val = Q1_val - cut_off_val, Q3_val + cut_off_val

    new_columns = [
        'Name of columns',
        'Min',
        'Q1',
        'Median',
        'Q3',
        'Max',
        'IQR',
        'Lower fence',
        'Upper fence',
        'Skew',
        'Number_of_outliers',
        'Percentage_of_outliers'
    ]
    data = zip(
        [column for column in df[columns]],
        min_val,
        Q1_val,
        median_val,
        Q3_val,
        max_val,
        IQR_val,
        lower_val,
        upper_val,
        skew_val,
        outliers_val,
        percentage(outliers_val)
    )
    new_df = pd.DataFrame(data=data, columns=new_columns)
    new_df.set_index('Name of columns', inplace=True)
    return new_df.sort_values('Number_of_outliers', ascending=False).transpose()
