"""AutoInsight EDA — Landing Page & File Upload."""

import streamlit as st
from pathlib import Path
from utils.loader import load_data

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AutoInsight EDA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ───────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Sidebar branding ────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 AutoInsight EDA")
    st.caption("Automatic Exploratory Data Analysis")
    st.divider()
    st.markdown(
        "Upload a dataset on the **Home** page, then navigate "
        "through the sidebar to explore your data."
    )

# ── Main content ────────────────────────────────────────────
st.markdown(
    """
    # 📊 AutoInsight EDA
    > **Upload your dataset and let AutoInsight do the heavy lifting.**
    """
)

st.divider()

# ── File uploader ────────────────────────────────────────────
uploaded = st.file_uploader(
    "📂  Drop your CSV or Excel file here",
    type=["csv", "xlsx", "xls"],
    help="Supported formats: .csv, .xlsx, .xls",
)

if uploaded:
    # Load and persist in session state
    df = load_data(uploaded)
    st.session_state["df"] = df
    st.session_state["filename"] = uploaded.name

    st.success(f"✅  **{uploaded.name}** loaded successfully!")
    st.divider()

    # Quick overview metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", f"{df.shape[1]:,}")
    col3.metric("Missing Cells", f"{int(df.isnull().sum().sum()):,}")
    col4.metric("Duplicates", f"{int(df.duplicated().sum()):,}")

    st.divider()

    # Preview
    st.subheader("🔍 Data Preview")
    preview_rows = st.slider("Rows to display", 5, 100, 10)
    st.dataframe(df.head(preview_rows), use_container_width=True)

    st.info("👈 **Navigate the sidebar** to explore Summary, Cleaning, Visualizations, Correlations, Outliers, and Reports.")

else:
    # Empty state
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 20px; opacity: 0.6;">
            <h2>🚀 Get Started</h2>
            <p style="font-size:1.1rem;">Upload a CSV or Excel file above to begin your analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
