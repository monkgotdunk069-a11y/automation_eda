"""Outlier detection utilities — IQR and Z-score methods."""

import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import plotly.express as px
from scipy import stats


def detect_iqr(df: pd.DataFrame, column: str):
    """Detect outliers using the IQR method.

    Returns
    -------
    tuple[pd.Series, float, float]
        (boolean mask where True = outlier, lower_bound, upper_bound)
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (df[column] < lower) | (df[column] > upper)
    return mask, lower, upper


def detect_zscore(df: pd.DataFrame, column: str, threshold: float = 3.0):
    """Detect outliers using the Z-score method.

    Returns
    -------
    tuple[pd.Series, pd.Series]
        (boolean mask where True = outlier, z-score values)
    """
    z = np.abs(stats.zscore(df[column].dropna()))
    # Align z-scores back to the original index
    z_full = pd.Series(np.nan, index=df.index)
    z_full.loc[df[column].dropna().index] = z
    mask = z_full.abs() > threshold
    return mask, z_full


def get_outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return an outlier summary table for all numeric columns (IQR method).

    Columns: Column, Outlier Count, Outlier %, Lower Bound, Upper Bound.
    """
    numeric_cols = df.select_dtypes(include="number").columns
    records = []
    for col in numeric_cols:
        mask, lower, upper = detect_iqr(df, col)
        count = int(mask.sum())
        pct = round(count / len(df) * 100, 2) if len(df) else 0
        records.append({
            "Column": col,
            "Outlier Count": count,
            "Outlier %": pct,
            "Lower Bound": round(lower, 2),
            "Upper Bound": round(upper, 2),
        })
    return pd.DataFrame(records)


def plot_outliers(df: pd.DataFrame, column: str, method: str = "iqr"):
    """Box / strip plot with outliers highlighted.

    Parameters
    ----------
    method : str
        'iqr' or 'zscore'.
    """
    temp = df[[column]].dropna().copy()

    if method == "iqr":
        mask, _, _ = detect_iqr(df, column)
    else:
        mask, _ = detect_zscore(df, column)

    temp = temp.loc[mask.index]
    temp["Outlier"] = mask.astype(str).map({"True": "Yes", "False": "No"})

    fig = px.strip(
        temp,
        y=column,
        color="Outlier",
        color_discrete_map={"Yes": "#e94560", "No": "#00D4AA"},
        stripmode="overlay",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        title=f"Outliers in {column} ({method.upper()})",
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig
