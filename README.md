# 📊 AutoInsight EDA

**Automatic Exploratory Data Analysis** — Upload a CSV or Excel file and get instant, interactive insights.

## Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Upload dataset, quick preview & metrics |
| 📋 **Summary** | Shape, dtypes, memory, per-column statistics |
| 🧹 **Cleaning** | Handle missing values, remove duplicates, cast types, download cleaned data |
| 📊 **Visualization** | Distribution, box plots, scatter plots, bar charts (Plotly) |
| 🔗 **Correlation** | Heatmap, top correlated pairs, Pearson / Spearman / Kendall |
| 🔍 **Outliers** | IQR & Z-score detection, visual highlighting, one-click removal |
| 📄 **Report** | Generate & download a comprehensive PDF report |

## Quick Start

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

## Tech Stack

- **Streamlit** — UI framework
- **Pandas / NumPy** — Data wrangling
- **Plotly** — Interactive charts
- **SciPy** — Statistical analysis
- **ReportLab** — PDF generation
- **Missingno / Seaborn / Matplotlib** — Additional visualization support

## Project Structure

```
AutoInsight_EDA/
├── app.py                     # Landing page
├── pages/                     # Streamlit multi-page app
│   ├── 1_📋_Summary.py
│   ├── 2_🧹_Cleaning.py
│   ├── 3_📊_Visualization.py
│   ├── 4_🔗_Correlation.py
│   ├── 5_🔍_Outliers.py
│   └── 6_📄_Report.py
├── utils/                     # Business logic (no UI code)
│   ├── loader.py
│   ├── cleaning.py
│   ├── summary.py
│   ├── visualization.py
│   ├── correlation.py
│   ├── outlier.py
│   └── report.py
├── assets/
│   └── style.css              # Custom dark theme
├── requirements.txt
└── README.md
```

## License

MIT
