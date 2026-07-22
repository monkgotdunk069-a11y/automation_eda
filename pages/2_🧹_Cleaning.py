"""Page 2 — Data Cleaning."""

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.cleaning import (
    get_missing_info,
    drop_missing_columns,
    drop_missing_rows,
    fill_missing,
    remove_duplicates,
    cast_column,
)
from utils.visualization import plot_missing_matrix

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Cleaning | AutoInsight", page_icon="🧹", layout="wide")

css_path = Path(__file__).parents[1] / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("# 🧹 Data Cleaning")
st.divider()

if "df" not in st.session_state:
    st.warning("⚠️  Please upload a dataset on the **Home** page first.")
    st.stop()

# Work on a copy so original stays intact
if "df_clean" not in st.session_state:
    st.session_state["df_clean"] = st.session_state["df"].copy()

df = st.session_state["df_clean"]

# ── Tabs ─────────────────────────────────────────────────────
tab_missing, tab_duplicates, tab_types = st.tabs([
    "🔳 Missing Values", "📑 Duplicates", "🔄 Type Casting"
])

# ══════════════════════════════════════════════════════════════
#  TAB 1 — Missing Values
# ══════════════════════════════════════════════════════════════
with tab_missing:
    missing_info = get_missing_info(df)
    has_missing = missing_info[missing_info["Missing Count"] > 0]

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("### Missing Values Table")
        if len(has_missing) > 0:
            st.dataframe(has_missing, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No missing values found!")

    with col_b:
        st.markdown("### Missing Value Matrix")
        if int(df.isnull().sum().sum()) > 0:
            fig = plot_missing_matrix(df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nothing to show — dataset is complete.")

    st.divider()

    if len(has_missing) > 0:
        st.markdown("### 🛠️ Fix Missing Values")

        fix_col1, fix_col2 = st.columns(2)

        with fix_col1:
            st.markdown("**Drop columns by threshold**")
            threshold = st.slider(
                "Max missing % allowed", 0, 100, 50, key="drop_thresh"
            )
            if st.button("Drop columns", key="btn_drop_cols"):
                df = drop_missing_columns(df, threshold)
                st.session_state["df_clean"] = df
                st.success(f"Dropped columns with >{threshold}% missing.")
                st.rerun()

            st.markdown("**Drop rows with any missing**")
            drop_subset = st.multiselect(
                "Select columns (leave empty for all)",
                options=df.columns.tolist(),
                key="drop_row_cols",
            )
            if st.button("Drop rows", key="btn_drop_rows"):
                subset = drop_subset if drop_subset else None
                df = drop_missing_rows(df, subset)
                st.session_state["df_clean"] = df
                st.success("Dropped rows with missing values.")
                st.rerun()

        with fix_col2:
            st.markdown("**Fill missing values**")
            cols_with_missing = has_missing["Column"].tolist()
            fill_col = st.selectbox("Column", cols_with_missing, key="fill_col")
            strategy = st.selectbox(
                "Strategy",
                ["mean", "median", "mode", "ffill", "bfill", "custom"],
                key="fill_strategy",
            )
            custom_val = None
            if strategy == "custom":
                custom_val = st.text_input("Custom value", key="fill_custom")
            if st.button("Fill missing", key="btn_fill"):
                df = fill_missing(df, fill_col, strategy, custom_val)
                st.session_state["df_clean"] = df
                st.success(f"Filled missing in **{fill_col}** with **{strategy}**.")
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  TAB 2 — Duplicates
# ══════════════════════════════════════════════════════════════
with tab_duplicates:
    dup_count = int(df.duplicated().sum())
    st.metric("Duplicate Rows", f"{dup_count:,}")

    if dup_count > 0:
        with st.expander("Preview duplicate rows"):
            st.dataframe(df[df.duplicated(keep=False)].head(50), use_container_width=True)

        if st.button("Remove Duplicates", key="btn_dedup"):
            df = remove_duplicates(df)
            st.session_state["df_clean"] = df
            st.success(f"Removed {dup_count} duplicate rows.")
            st.rerun()
    else:
        st.success("✅ No duplicate rows found!")

# ══════════════════════════════════════════════════════════════
#  TAB 3 — Type Casting
# ══════════════════════════════════════════════════════════════
with tab_types:
    st.markdown("### Current Data Types")
    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Current Type": df.dtypes.astype(str).values,
    })
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 🔄 Cast Column Type")

    tc1, tc2 = st.columns(2)
    with tc1:
        cast_col = st.selectbox("Column to cast", df.columns, key="cast_col")
    with tc2:
        target_type = st.selectbox(
            "Target type",
            ["int", "float", "str", "datetime", "category"],
            key="cast_type",
        )

    if st.button("Cast", key="btn_cast"):
        df = cast_column(df, cast_col, target_type)
        st.session_state["df_clean"] = df
        st.success(f"Cast **{cast_col}** → **{target_type}**")
        st.rerun()

# ── Footer: Download cleaned dataset ─────────────────────────
st.divider()

col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1])
with col_dl1:
    st.markdown(f"**Cleaned shape:** {df.shape[0]:,} rows × {df.shape[1]:,} columns")
with col_dl2:
    if st.button("↩️ Reset to Original", key="btn_reset"):
        st.session_state["df_clean"] = st.session_state["df"].copy()
        st.rerun()
with col_dl3:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Cleaned CSV", csv, "cleaned_data.csv", "text/csv")
