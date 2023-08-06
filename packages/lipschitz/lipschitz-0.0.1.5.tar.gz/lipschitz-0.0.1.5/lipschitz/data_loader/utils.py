import pandas as pd
import numpy as np

def get_data_column(data_column, df, start_index: int, end_index: int):
    """
    Calculating or fetching data column, filter by [start_index, end_index]

    Parameters
    ----------
    data_column : str or Factor
    df : pd.DataFrame
    start_index : int
        inclusive
    end_index : int
        inclusive

    Return
    ------
    set of two pd.DataFrame
        X and y training set.
    """
    if (type(data_column) == str):
        return df.iloc[start_index:end_index][data_column]
    elif (data_column.method == "sma"):
        return simple_moving_average(data_column, df, start_index, end_index)
    elif (data_column.method == "pct_change_sign"):
        return pct_change_sign(data_column, df, start_index, end_index)
    elif (data_column.method == "pct_change"):
        return pct_change(data_column, df, start_index, end_index)

def pct_change(factor, df: pd.DataFrame, start_index: int, end_index: int) -> pd.Series:
    factor_window = df.iloc[max(start_index-1, 0):end_index][factor.column_name]
    return factor_window.pct_change().iloc[1:]

def pct_change_sign(factor, df, start_index:int, end_index:int) -> pd.Series:
    factor_window = df.iloc[max(start_index-1, 0):end_index][factor.column_name]
    pct_change_sign = (np.sign(factor_window.pct_change().iloc[1:] - 1e-8) + 1)/2 # Treat 0 as down
    pct_change_sign = pct_change_sign.astype(int)
    pct_change_sign = pd.Series(pct_change_sign, index=factor_window.index[1:])
    return pct_change_sign

def simple_moving_average(factor, df, start_index: int, end_index: int):
    """
    Calculating simple moving average, filter by [start_index, end_index]

    Parameters
    ----------
    factor : Factor
    df : pd.DataFrame
    start_index : int
        inclusive
    end_index : int
        inclusive

    Return
    ------
    pd.Series
    """
    # FIXME: start_index - factor.window_size + 1 could be less than 0
    return df.iloc[start_index - factor.window_size + 1:end_index][factor.column_name].rolling(window=factor.window_size).mean().iloc[factor.window_size-1:]
