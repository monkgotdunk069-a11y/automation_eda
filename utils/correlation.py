"""Correlation analysis utilities."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def get_correlation_matrix(
    df: pd.DataFrame, method: str = "pearson"
) -> pd.DataFrame:
    """Compute the correlation matrix for numeric columns.

    Parameters
    ----------
    method : str
        'pearson', 'spearman', or 'kendall'.
    """
    numeric = df.select_dtypes(include="number")
    return numeric.corr(method=method)


def plot_heatmap(corr: pd.DataFrame):
    """Interactive Plotly annotated heatmap of a correlation matrix."""
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    corr_masked = corr.where(~mask)

    fig = go.Figure(
        data=go.Heatmap(
            z=corr_masked.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale="RdBu_r",
            zmin=-1,
            zmax=1,
            text=corr_masked.round(2).values,
            texttemplate="%{text}",
            textfont=dict(size=11),
            hovertemplate="%{x} vs %{y}: %{z:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        title="Correlation Heatmap",
        margin=dict(l=40, r=20, t=50, b=40),
        height=600,
    )
    return fig


def get_top_correlations(corr: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top-N most correlated pairs (absolute value, excl. diagonal).

    Returns
    -------
    pd.DataFrame
        Columns: Feature 1, Feature 2, Correlation.
    """
    # Unstack and remove duplicates + self-correlations
    unstacked = corr.where(
        np.triu(np.ones_like(corr, dtype=bool), k=1)
    ).stack()
    unstacked = unstacked.reset_index()
    unstacked.columns = ["Feature 1", "Feature 2", "Correlation"]
    unstacked["Abs"] = unstacked["Correlation"].abs()
    top = (
        unstacked.sort_values("Abs", ascending=False)
        .head(n)
        .drop(columns="Abs")
        .reset_index(drop=True)
    )
    top["Correlation"] = top["Correlation"].round(4)
    return top
