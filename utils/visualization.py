"""Visualization builders using Plotly."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# Shared layout defaults
# ---------------------------------------------------------------------------
_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif"),
    margin=dict(l=40, r=20, t=50, b=40),
)

_COLORSCALE = px.colors.sequential.Tealgrn


def _apply_layout(fig, title: str = ""):
    """Apply the common dark layout to a figure."""
    fig.update_layout(**_LAYOUT, title=title)
    return fig


# ---------------------------------------------------------------------------
# Distribution
# ---------------------------------------------------------------------------
def plot_distribution(df: pd.DataFrame, column: str):
    """Histogram + KDE overlay for a numeric column."""
    fig = px.histogram(
        df,
        x=column,
        marginal="box",
        color_discrete_sequence=["#00D4AA"],
        opacity=0.8,
    )
    return _apply_layout(fig, f"Distribution of {column}")


# ---------------------------------------------------------------------------
# Box plot
# ---------------------------------------------------------------------------
def plot_boxplot(df: pd.DataFrame, column: str):
    """Horizontal box plot for a numeric column."""
    fig = px.box(
        df,
        x=column,
        color_discrete_sequence=["#7C4DFF"],
        points="outliers",
    )
    return _apply_layout(fig, f"Box Plot — {column}")


# ---------------------------------------------------------------------------
# Scatter
# ---------------------------------------------------------------------------
def plot_scatter(df: pd.DataFrame, x: str, y: str, hue: str | None = None):
    """Scatter plot with optional colour dimension."""
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=hue,
        color_discrete_sequence=px.colors.qualitative.Set2,
        opacity=0.7,
    )
    return _apply_layout(fig, f"{y} vs {x}")


# ---------------------------------------------------------------------------
# Bar chart (numeric value counts)
# ---------------------------------------------------------------------------
def plot_bar(df: pd.DataFrame, column: str, top_n: int = 20):
    """Bar chart of value counts for a column (top N)."""
    vc = df[column].value_counts().head(top_n).reset_index()
    vc.columns = [column, "Count"]
    fig = px.bar(
        vc,
        x=column,
        y="Count",
        color="Count",
        color_continuous_scale="Tealgrn",
    )
    return _apply_layout(fig, f"Value Counts — {column}")


# ---------------------------------------------------------------------------
# Count plot (categorical)
# ---------------------------------------------------------------------------
def plot_countplot(df: pd.DataFrame, column: str, top_n: int = 20):
    """Horizontal bar chart for categorical value counts."""
    vc = df[column].value_counts().head(top_n).reset_index()
    vc.columns = [column, "Count"]
    fig = px.bar(
        vc,
        y=column,
        x="Count",
        orientation="h",
        color="Count",
        color_continuous_scale="Purp",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return _apply_layout(fig, f"Count Plot — {column}")


# ---------------------------------------------------------------------------
# Missing-value matrix
# ---------------------------------------------------------------------------
def plot_missing_matrix(df: pd.DataFrame):
    """Heatmap-style missing-value matrix (white = present, dark = missing)."""
    missing = df.isnull().astype(int)
    fig = go.Figure(
        data=go.Heatmap(
            z=missing.values,
            x=missing.columns.tolist(),
            y=list(range(len(missing))),
            colorscale=[[0, "#1a1a2e"], [1, "#e94560"]],
            showscale=False,
        )
    )
    fig.update_layout(
        yaxis=dict(title="Row index", autorange="reversed"),
        xaxis=dict(title=""),
    )
    return _apply_layout(fig, "Missing Value Matrix")
