"""Page 5 — Outlier Detection."""

import streamlit as st
from pathlib import Path
from utils.outlier import (
    detect_iqr,
    detect_zscore,
    get_outlier_summary,
    plot_outliers,
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Outliers | AutoInsight", page_icon="🔍", layout="wide")

css_path = Path(__file__).parents[1] / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("# 🔍 Outlier Detection")
st.divider()

if "df" not in st.session_state:
    st.warning("⚠️  Please upload a dataset on the **Home** page first.")
    st.stop()

df = st.session_state.get("df_clean", st.session_state["df"])
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    st.info("No numeric columns available for outlier detection.")
    st.stop()

# ── Summary table ────────────────────────────────────────────
st.subheader("📋 Outlier Summary (IQR Method)")
summary = get_outlier_summary(df)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.divider()

# ── Per-column explorer ──────────────────────────────────────
st.subheader("🔬 Explore Column")

ctrl1, ctrl2 = st.columns(2)
with ctrl1:
    col = st.selectbox("Column", numeric_cols, key="outlier_col")
with ctrl2:
    method = st.selectbox("Method", ["iqr", "zscore"], key="outlier_method")

# Detection
if method == "iqr":
    mask, lower, upper = detect_iqr(df, col)
    st.markdown(f"**Bounds:** Lower = `{lower:.2f}` · Upper = `{upper:.2f}`")
else:
    z_thresh = st.slider("Z-score threshold", 1.0, 5.0, 3.0, 0.1, key="z_thresh")
    mask, z_scores = detect_zscore(df, col, z_thresh)

outlier_count = int(mask.sum())
total = len(df)

m1, m2, m3 = st.columns(3)
m1.metric("Total Rows", f"{total:,}")
m2.metric("Outliers", f"{outlier_count:,}")
m3.metric("Outlier %", f"{round(outlier_count / total * 100, 2)}%")

# Plot
fig = plot_outliers(df, col, method)
st.plotly_chart(fig, use_container_width=True)

# ── Option to remove outliers ─────────────────────────────────
st.divider()
if outlier_count > 0:
    with st.expander("👁️ Preview outlier rows"):
        st.dataframe(df[mask].head(50), use_container_width=True)

    if st.button(f"🗑️ Remove {outlier_count} outliers from **{col}**", key="btn_rm_outliers"):
        df_cleaned = df[~mask].reset_index(drop=True)
        st.session_state["df_clean"] = df_cleaned
        st.success(f"Removed {outlier_count} outliers from **{col}**.")
        st.rerun()
else:
    st.success(f"✅ No outliers detected in **{col}** with {method.upper()} method.")
