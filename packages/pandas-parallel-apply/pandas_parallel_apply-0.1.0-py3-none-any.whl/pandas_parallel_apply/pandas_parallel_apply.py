"""General module for parallelizing a dataframe apply function on a column (series) or entire row"""

import logging
from tqdm import tqdm
from multiprocessing import Pool
import numpy as np
import pandas as pd
from typing import Callable
from functools import partial

tqdm.pandas()


def parallelize_dataframe(df: pd.DataFrame, func: Callable, n_cores: int) -> pd.DataFrame:
    """Function used to split a dataframe in n sub dataframes, based on the number of cores we want to use."""
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

"""
Apply on column
Usage:
    standard => df[col_name].apply(f)
    serial   => apply_on_df_col(df, col_name, f)
    parallel => parallelize_dataframe(df, partial(apply_on_df_col, col_name=col_name, f=f), n_cores)
             => apply_on_df_col_parallel(df, col_name, f, n_cores)
    switch   => apply_on_df_col_maybe_parallel(df, col_name, f, true/false, n_cores)
"""


def apply_on_df_col(df: pd.DataFrame, col_name: str, f: Callable, pbar: bool = True) -> pd.Series:
    """Simple wrapper on top of df[col].apply(x) using tqdm. Used by the parallel version of this process."""
    if pbar:
        return df[col_name].progress_apply(f)
    else:
        return df[col_name].apply(f)


def apply_on_df_col_parallel(df: pd.DataFrame, col_name: str, f: Callable,
                             n_cores: int, pbar: bool = True) -> pd.Series:
    """Function call the df.apply(f) chain in parallel """
    logging.debug(f"Parallelizing apply on df (rows: {len(df)}) on column '{col_name}' with {n_cores} cores")
    return parallelize_dataframe(df, partial(apply_on_df_col, col_name=col_name, f=f), n_cores)


def apply_on_df_col_maybe_parallel(df: pd.DataFrame, col_name: str, f: Callable,
                                   parallel: bool, n_cores: int, pbar: bool = True):
    """Wrapper on top of apply_on_df_col"""
    if parallel:
        return apply_on_df_col_parallel(df, col_name, f, n_cores, pbar)
    else:
        return apply_on_df_col(df, col_name, f, pbar)


"""
Apply on row
Usage:
    standard => df.apply(f, axis=1)
    serial   => apply_on_df(df, f)
    parallel => parallelize_dataframe(df, partial(apply_on_df, f=f), n_cores)
             => apply_on_df_parallel(df, f, n_cores)
    switch   => apply_on_df_maybe_parallel(df, f, true/false, n_cores)
"""

def apply_on_df(df: pd.DataFrame, f: Callable, pbar: bool = True) -> pd.Series:
    """Apply a function on each row (all possible columns), returning a series"""
    if pbar:
        return df.progress_apply(f, axis=1)
    else:
        return df.apply(f, axis=1)


def apply_on_df_parallel(df: pd.DataFrame, f: Callable, n_cores: int, pbar: bool = True) -> pd.Series:
    """Function to call df.apply(f, axis=1) in parallel on n cores"""
    logging.debug(f"Parallelizing apply on df (rows: {len(df)}) with {n_cores} cores")
    return parallelize_dataframe(df, partial(apply_on_df, f=f), n_cores)


def apply_on_df_maybe_parallel(df: pd.DataFrame, f: Callable, parallel: bool,
                               n_cores: int, pbar: bool = True) -> pd.Series:
    """Wrapper on top of apply_on_df"""
    if parallel:
        return apply_on_df_parallel(df, f, n_cores, pbar)
    else:
        return apply_on_df(df, f, pbar)
