"""Dataset summary and statistics utilities."""

import pandas as pd


def get_overview(df: pd.DataFrame) -> dict:
    """Return a high-level overview of the dataset.

    Returns
    -------
    dict
        Keys: rows, columns, memory_mb, duplicates, missing_cells, missing_pct,
              numeric_cols, categorical_cols.
    """
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = int(df.isnull().sum().sum())
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(exclude="number").columns.tolist()

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        "duplicates": int(df.duplicated().sum()),
        "missing_cells": missing_cells,
        "missing_pct": round(missing_cells / total_cells * 100, 2) if total_cells else 0,
        "numeric_cols": len(numeric),
        "categorical_cols": len(categorical),
    }


def get_column_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-column statistics combining describe(), missing %, and unique counts.

    Returns
    -------
    pd.DataFrame
        One row per column with stats: type, missing count, missing %, unique,
        mean/std/min/max for numerics, top/freq for categoricals.
    """
    records = []
    for col in df.columns:
        series = df[col]
        missing_count = int(series.isnull().sum())
        missing_pct = round(missing_count / len(df) * 100, 2) if len(df) else 0
        unique = int(series.nunique())

        row = {
            "Column": col,
            "Type": str(series.dtype),
            "Missing": missing_count,
            "Missing %": missing_pct,
            "Unique": unique,
        }

        if pd.api.types.is_numeric_dtype(series):
            row["Mean"] = round(series.mean(), 2) if not series.dropna().empty else None
            row["Std"] = round(series.std(), 2) if not series.dropna().empty else None
            row["Min"] = series.min() if not series.dropna().empty else None
            row["Max"] = series.max() if not series.dropna().empty else None
        else:
            vc = series.value_counts()
            row["Top"] = vc.index[0] if len(vc) > 0 else None
            row["Freq"] = int(vc.iloc[0]) if len(vc) > 0 else None

        records.append(row)

    return pd.DataFrame(records)
