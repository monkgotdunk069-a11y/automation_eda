"""PDF report generation using ReportLab."""

import io
import datetime
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from utils.summary import get_overview, get_column_stats
from utils.cleaning import get_missing_info
from utils.outlier import get_outlier_summary


def _heading(text: str, styles):
    return Paragraph(text, styles["Heading2"])


def _body(text: str, styles):
    return Paragraph(text, styles["BodyText"])


def _df_to_table(df: pd.DataFrame, max_rows: int = 30):
    """Convert a DataFrame to a ReportLab Table (header + rows)."""
    df = df.head(max_rows)
    data = [df.columns.tolist()] + df.astype(str).values.tolist()

    col_count = len(df.columns)
    col_width = min(480 / col_count, 120)

    table = Table(data, colWidths=[col_width] * col_count)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f5f5f5"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def generate_pdf_report(df: pd.DataFrame) -> bytes:
    """Generate a full EDA PDF report and return it as bytes.

    Returns
    -------
    bytes
        PDF content ready for download.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()

    # Custom title style
    styles.add(ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=20,
        textColor=colors.HexColor("#1a1a2e"),
    ))

    elements: list = []

    # ---- Title page ----
    elements.append(Paragraph("AutoInsight EDA Report", styles["ReportTitle"]))
    elements.append(_body(
        f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles,
    ))
    elements.append(Spacer(1, 12))

    # ---- Overview ----
    overview = get_overview(df)
    elements.append(_heading("1. Dataset Overview", styles))
    overview_text = (
        f"Rows: {overview['rows']} &nbsp;|&nbsp; Columns: {overview['columns']} &nbsp;|&nbsp; "
        f"Memory: {overview['memory_mb']} MB<br/>"
        f"Duplicates: {overview['duplicates']} &nbsp;|&nbsp; "
        f"Missing cells: {overview['missing_cells']} ({overview['missing_pct']}%)<br/>"
        f"Numeric columns: {overview['numeric_cols']} &nbsp;|&nbsp; "
        f"Categorical columns: {overview['categorical_cols']}"
    )
    elements.append(_body(overview_text, styles))
    elements.append(Spacer(1, 10))

    # ---- Column statistics ----
    elements.append(_heading("2. Column Statistics", styles))
    col_stats = get_column_stats(df)
    elements.append(_df_to_table(col_stats))
    elements.append(Spacer(1, 10))

    # ---- Missing values ----
    elements.append(_heading("3. Missing Values", styles))
    missing_info = get_missing_info(df)
    has_missing = missing_info[missing_info["Missing Count"] > 0]
    if len(has_missing) > 0:
        elements.append(_df_to_table(has_missing))
    else:
        elements.append(_body("No missing values found. ✓", styles))
    elements.append(Spacer(1, 10))

    # ---- Descriptive statistics ----
    elements.append(PageBreak())
    elements.append(_heading("4. Descriptive Statistics (Numeric)", styles))
    desc = df.describe().T.reset_index().rename(columns={"index": "Column"})
    desc = desc.round(2)
    elements.append(_df_to_table(desc))
    elements.append(Spacer(1, 10))

    # ---- Outlier summary ----
    elements.append(_heading("5. Outlier Summary (IQR)", styles))
    outlier_summary = get_outlier_summary(df)
    if len(outlier_summary) > 0:
        elements.append(_df_to_table(outlier_summary))
    else:
        elements.append(_body("No numeric columns to analyse.", styles))
    elements.append(Spacer(1, 10))

    # ---- Data sample ----
    elements.append(_heading("6. Data Sample (First 20 Rows)", styles))
    elements.append(_df_to_table(df.head(20)))

    # Build
    doc.build(elements)
    buf.seek(0)
    return buf.read()
