"""AutoInsight EDA utilities package."""

from utils.loader import load_data
from utils.cleaning import (
    get_missing_info,
    drop_missing_columns,
    drop_missing_rows,
    fill_missing,
    remove_duplicates,
    cast_column,
)
from utils.summary import get_overview, get_column_stats
from utils.visualization import (
    plot_distribution,
    plot_boxplot,
    plot_scatter,
    plot_bar,
    plot_countplot,
    plot_missing_matrix,
)
from utils.correlation import (
    get_correlation_matrix,
    plot_heatmap,
    get_top_correlations,
)
from utils.outlier import (
    detect_iqr,
    detect_zscore,
    get_outlier_summary,
    plot_outliers,
)
from utils.report import generate_pdf_report
