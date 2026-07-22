"""Page 6 — PDF Report Download."""

import streamlit as st
from pathlib import Path
from utils.report import generate_pdf_report

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Report | AutoInsight", page_icon="📄", layout="wide")

css_path = Path(__file__).parents[1] / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("# 📄 EDA Report")
st.divider()

if "df" not in st.session_state:
    st.warning("⚠️  Please upload a dataset on the **Home** page first.")
    st.stop()

df = st.session_state.get("df_clean", st.session_state["df"])
filename = st.session_state.get("filename", "dataset")

st.markdown(
    """
    Generate a comprehensive **PDF report** of your dataset analysis.
    The report includes:

    - 📋 Dataset overview (rows, columns, memory, missing values)
    - 📈 Column statistics (types, missing %, unique counts, descriptive stats)
    - 🔳 Missing value breakdown
    - 📊 Descriptive statistics for numeric columns
    - 🔍 Outlier summary (IQR method)
    - 🔢 Data sample (first 20 rows)
    """
)

st.divider()

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Rows", f"{df.shape[0]:,}")
    st.metric("Columns", f"{df.shape[1]:,}")

with col2:
    st.info("Click the button below to generate and download your report.")

    if st.button("🚀 Generate PDF Report", key="btn_gen_report", type="primary"):
        with st.spinner("Generating report…"):
            pdf_bytes = generate_pdf_report(df)
        st.success("✅ Report generated!")
        report_name = filename.rsplit(".", 1)[0] + "_eda_report.pdf"
        st.download_button(
            "⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name=report_name,
            mime="application/pdf",
        )
