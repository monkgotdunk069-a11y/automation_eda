"""Data loading utilities for CSV and Excel files."""

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(file) -> pd.DataFrame:
    """Load a CSV or Excel file into a DataFrame.

    Parameters
    ----------
    file : UploadedFile
        A Streamlit UploadedFile object (.csv or .xlsx).

    Returns
    -------
    pd.DataFrame
        The loaded dataset.
    """
    name = file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file type: {name}")
    return df
