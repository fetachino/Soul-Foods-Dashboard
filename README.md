# Soul Foods Pink Morsel Sales Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-3.x-008DE5?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Tests](https://github.com/fetachino/Soul-Foods-Dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/fetachino/Soul-Foods-Dashboard/actions/workflows/tests.yml)

An interactive sales analytics dashboard that transforms raw Soul Foods transaction
data into a focused view of **Pink Morsel revenue by date and region**. The project
demonstrates an end-to-end Python workflow: data ingestion and cleaning, derived
metric calculation, interactive visualization, responsive presentation, and
browser-level automated testing.

## Project highlights

- Combines three raw sales datasets into one analysis-ready dataset.
- Filters 41,160 source transactions down to 5,880 Pink Morsel records.
- Calculates revenue as `quantity × price` and exports a clean three-column CSV.
- Presents date-sorted sales in an interactive Plotly line chart.
- Filters the visualization across `north`, `east`, `south`, `west`, and `all`.
- Includes responsive custom CSS and a recruiter-friendly user interface.
- Verifies the header, chart, and region picker with Pytest and real browser tests.
- Provides a defensive Bash test runner suitable for local checks or CI workflows.

## Dashboard behavior

The application loads the generated Pink Morsel dataset and aggregates revenue by
date. Selecting a region updates the chart immediately; selecting **all** combines
revenue across every region. The graph includes descriptive date and sales axes,
markers, unified hover details, and a region-aware title.

## Technology stack

| Area | Tools |
| --- | --- |
| Data processing | Python, pandas |
| Web application | Dash, Flask |
| Visualization | Plotly Express |
| Testing | Pytest, Dash testing, Selenium, Chrome |
| Automation | Bash, virtual environments |

## Data pipeline

```text
3 raw daily_sales_data CSV files
              │
              ▼
     Combine all transactions
              │
              ▼
      Keep Pink Morsel rows
              │
              ▼
  sales = quantity × numeric price
              │
              ▼
 sales, date, region → formatted_sales_data.csv
```

The pipeline is implemented in `data_processor.py`. It validates that exactly three
input files are present, normalizes product and region values, parses prices and
dates, sorts the result, and writes:

```text
data/formatted_sales_data.csv
```

## Repository structure

```text
Soul-Foods-Dashboard/
├── app.py                         # Dash layout, chart, and region callback
├── data_processor.py              # Raw-data transformation pipeline
├── requirements.txt               # Reproducible runtime and test dependencies
├── pytest.ini                     # Pytest discovery configuration
├── run_tests.sh                   # Cross-platform Bash/virtualenv test runner
├── assets/
│   └── styles.css                 # Responsive dashboard styling
├── data/
│   ├── daily_sales_data_0.csv     # Raw source data
│   ├── daily_sales_data_1.csv
│   ├── daily_sales_data_2.csv
│   └── formatted_sales_data.csv   # Generated Pink Morsel dataset
└── tests/
    └── test_dash_app.py           # Three browser-level UI tests
```

## Getting started

### Prerequisites

- Python 3.11 or a compatible recent Python 3 release
- Google Chrome for the browser test suite
- Bash to use `run_tests.sh`

### macOS or Linux

```bash
git clone https://github.com/fetachino/Soul-Foods-Dashboard.git
cd Soul-Foods-Dashboard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python data_processor.py
python app.py
```

### Windows PowerShell

```powershell
git clone https://github.com/fetachino/Soul-Foods-Dashboard.git
Set-Location Soul-Foods-Dashboard
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python data_processor.py
python app.py
```

Open the local URL printed by Dash, typically <http://127.0.0.1:8050>.

The application also regenerates the formatted dataset automatically if the output
CSV is missing.

## Testing

The test suite launches the Dash application in Chrome and verifies that:

1. The Pink Morsel dashboard header is visible.
2. The Plotly visualization is rendered.
3. The region picker is visible and contains the required choices.

With the virtual environment created and dependencies installed, run:

```bash
./run_tests.sh
```

Expected result:

```text
collected 3 items
tests/test_dash_app.py ...
3 passed
All tests passed.
```

The runner detects `.venv` and `venv` layouts on Linux, macOS, Windows Git Bash,
and WSL. It exits with status `0` on success and `1` if activation, test execution,
or another required step fails.

## Design decisions

- **Separated transformation from presentation:** `data_processor.py` can rebuild
  the derived dataset independently of the web application.
- **Reproducible environments:** dependencies are declared in `requirements.txt`;
  virtual-environment contents and generated caches are excluded from Git.
- **Stable UI selectors:** explicit component IDs make both callbacks and browser
  tests readable and maintainable.
- **Defensive automation:** the test runner resolves its own repository path and
  handles common virtual-environment layouts before invoking Pytest.

## Data source

The three raw Soul Foods CSV files originate from the public
[Quantium Task 1 model-answer repository](https://github.com/vagabond-systems/quantium-task-1-model-answer).
This repository contains an independently organized implementation of the data
pipeline, dashboard, styling, automated tests, and test runner.
