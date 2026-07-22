"""Page 4 — Correlation Analysis."""

import streamlit as st
from pathlib import Path
from utils.correlation import get_correlation_matrix, plot_heatmap, get_top_correlations

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Correlation | AutoInsight", page_icon="🔗", layout="wide")

css_path = Path(__file__).parents[1] / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("# 🔗 Correlation Analysis")
st.divider()

if "df" not in st.session_state:
    st.warning("⚠️  Please upload a dataset on the **Home** page first.")
    st.stop()

df = st.session_state.get("df_clean", st.session_state["df"])
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if len(numeric_cols) < 2:
    st.info("Need at least 2 numeric columns for correlation analysis.")
    st.stop()

# ── Controls ─────────────────────────────────────────────────
ctrl1, ctrl2 = st.columns([1, 1])
with ctrl1:
    method = st.selectbox(
        "Correlation method",
        ["pearson", "spearman", "kendall"],
        key="corr_method",
    )
with ctrl2:
    top_n = st.slider("Top correlated pairs to show", 5, 30, 10, key="corr_topn")

st.divider()

# ── Heatmap ──────────────────────────────────────────────────
corr = get_correlation_matrix(df, method)

st.subheader("🔥 Correlation Heatmap")
fig = plot_heatmap(corr)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Top correlated pairs ─────────────────────────────────────
st.subheader(f"🏆 Top {top_n} Correlated Pairs")
top_pairs = get_top_correlations(corr, top_n)
st.dataframe(top_pairs, use_container_width=True, hide_index=True)

# ── Full matrix (expandable) ─────────────────────────────────
with st.expander("📄 Full Correlation Matrix"):
    st.dataframe(corr.round(3), use_container_width=True)
