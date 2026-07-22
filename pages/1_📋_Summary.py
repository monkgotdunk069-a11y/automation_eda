"""Page 1 — Dataset Summary & Column Statistics."""

import streamlit as st
from pathlib import Path
from utils.summary import get_overview, get_column_stats

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Summary | AutoInsight", page_icon="📋", layout="wide")

css_path = Path(__file__).parents[1] / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("# 📋 Dataset Summary")
st.divider()

# ── Guard: dataset required ──────────────────────────────────
if "df" not in st.session_state:
    st.warning("⚠️  Please upload a dataset on the **Home** page first.")
    st.stop()

df = st.session_state["df"]

# ── Overview metrics ─────────────────────────────────────────
overview = get_overview(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{overview['rows']:,}")
c2.metric("Columns", f"{overview['columns']:,}")
c3.metric("Memory", f"{overview['memory_mb']} MB")
c4.metric("Duplicates", f"{overview['duplicates']:,}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Missing Cells", f"{overview['missing_cells']:,}")
c6.metric("Missing %", f"{overview['missing_pct']}%")
c7.metric("Numeric Cols", overview["numeric_cols"])
c8.metric("Categorical Cols", overview["categorical_cols"])

st.divider()

# ── Column types breakdown ───────────────────────────────────
st.subheader("📊 Column Types")
col_types = df.dtypes.value_counts().reset_index()
col_types.columns = ["Data Type", "Count"]
st.dataframe(col_types, use_container_width=True, hide_index=True)

st.divider()

# ── Per-column statistics ────────────────────────────────────
st.subheader("📈 Column Statistics")
col_stats = get_column_stats(df)
st.dataframe(col_stats, use_container_width=True, hide_index=True, height=400)

st.divider()

# ── Data preview ─────────────────────────────────────────────
st.subheader("🔍 Data Preview")
n = st.slider("Rows to display", 5, min(100, len(df)), 10, key="summary_rows")
st.dataframe(df.head(n), use_container_width=True)
