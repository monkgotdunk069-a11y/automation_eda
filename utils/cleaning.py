"""Data cleaning utilities — missing values, duplicates, type casting."""

import pandas as pd
import numpy as np


def get_missing_info(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with missing-value statistics per column.

    Columns: Column, Missing Count, Missing %, Data Type.
    """
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    info = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing.values,
        "Missing %": pct.values,
        "Data Type": df.dtypes.astype(str).values,
    })
    return info.sort_values("Missing %", ascending=False).reset_index(drop=True)


def drop_missing_columns(df: pd.DataFrame, threshold: float = 50.0) -> pd.DataFrame:
    """Drop columns where missing % exceeds *threshold*.

    Parameters
    ----------
    df : pd.DataFrame
    threshold : float
        Maximum allowed missing percentage (0–100).

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with high-missing columns removed.
    """
    pct = df.isnull().sum() / len(df) * 100
    keep = pct[pct <= threshold].index.tolist()
    return df[keep].copy()


def drop_missing_rows(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Drop rows that contain any missing value in *columns*.

    If *columns* is None, drops rows with any missing value anywhere.
    """
    return df.dropna(subset=columns).reset_index(drop=True)


def fill_missing(
    df: pd.DataFrame,
    column: str,
    strategy: str = "mean",
    custom_value=None,
) -> pd.DataFrame:
    """Fill missing values in a single column.

    Parameters
    ----------
    strategy : str
        One of 'mean', 'median', 'mode', 'ffill', 'bfill', 'custom'.
    custom_value
        Used when strategy == 'custom'.
    """
    df = df.copy()
    if strategy == "mean":
        df[column] = df[column].fillna(df[column].mean())
    elif strategy == "median":
        df[column] = df[column].fillna(df[column].median())
    elif strategy == "mode":
        mode_val = df[column].mode()
        if len(mode_val) > 0:
            df[column] = df[column].fillna(mode_val.iloc[0])
    elif strategy == "ffill":
        df[column] = df[column].ffill()
    elif strategy == "bfill":
        df[column] = df[column].bfill()
    elif strategy == "custom":
        df[column] = df[column].fillna(custom_value)
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows and reset the index."""
    return df.drop_duplicates().reset_index(drop=True)


def cast_column(df: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    """Cast a column to a new data type.

    Parameters
    ----------
    dtype : str
        Target type — 'int', 'float', 'str', 'datetime', 'category'.
    """
    df = df.copy()
    try:
        if dtype == "datetime":
            df[column] = pd.to_datetime(df[column], errors="coerce")
        elif dtype == "category":
            df[column] = df[column].astype("category")
        elif dtype == "int":
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
        elif dtype == "float":
            df[column] = pd.to_numeric(df[column], errors="coerce")
        elif dtype == "str":
            df[column] = df[column].astype(str)
    except Exception:
        pass  # silently skip if cast fails — UI will show feedback
    return df
