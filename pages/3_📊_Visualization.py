"""Page 3 — Visualizations."""

import streamlit as st
from pathlib import Path
from utils.visualization import (
    plot_distribution,
    plot_boxplot,
    plot_scatter,
    plot_bar,
    plot_countplot,
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Visualization | AutoInsight", page_icon="📊", layout="wide")

css_path = Path(__file__).parents[1] / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("# 📊 Visualizations")
st.divider()

if "df" not in st.session_state:
    st.warning("⚠️  Please upload a dataset on the **Home** page first.")
    st.stop()

df = st.session_state.get("df_clean", st.session_state["df"])
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
all_cols = df.columns.tolist()

# ── Tabs ─────────────────────────────────────────────────────
tab_dist, tab_box, tab_scatter, tab_bar = st.tabs([
    "📈 Distribution", "📦 Box Plot", "🔵 Scatter", "📊 Bar / Count"
])

# ══════════════════════════════════════════════════════════════
#  Distribution
# ══════════════════════════════════════════════════════════════
with tab_dist:
    if not numeric_cols:
        st.info("No numeric columns available.")
    else:
        col = st.selectbox("Select numeric column", numeric_cols, key="dist_col")
        fig = plot_distribution(df, col)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  Box Plot
# ══════════════════════════════════════════════════════════════
with tab_box:
    if not numeric_cols:
        st.info("No numeric columns available.")
    else:
        selected_box = st.multiselect(
            "Select columns (up to 4)",
            numeric_cols,
            default=numeric_cols[:1],
            max_selections=4,
            key="box_cols",
        )
        if selected_box:
            cols = st.columns(min(len(selected_box), 2))
            for i, c in enumerate(selected_box):
                with cols[i % 2]:
                    fig = plot_boxplot(df, c)
                    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  Scatter
# ══════════════════════════════════════════════════════════════
with tab_scatter:
    if len(numeric_cols) < 2:
        st.info("Need at least 2 numeric columns for a scatter plot.")
    else:
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            x_col = st.selectbox("X axis", numeric_cols, key="scatter_x")
        with sc2:
            y_default = 1 if len(numeric_cols) > 1 else 0
            y_col = st.selectbox("Y axis", numeric_cols, index=y_default, key="scatter_y")
        with sc3:
            hue_options = ["None"] + categorical_cols
            hue = st.selectbox("Color by", hue_options, key="scatter_hue")
            hue = None if hue == "None" else hue

        fig = plot_scatter(df, x_col, y_col, hue)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  Bar / Count
# ══════════════════════════════════════════════════════════════
with tab_bar:
    bar_col = st.selectbox("Select column", all_cols, key="bar_col")
    top_n = st.slider("Top N values", 5, 50, 20, key="bar_topn")

    if bar_col in numeric_cols:
        fig = plot_bar(df, bar_col, top_n)
    else:
        fig = plot_countplot(df, bar_col, top_n)
    st.plotly_chart(fig, use_container_width=True)
