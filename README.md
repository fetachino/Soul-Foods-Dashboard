# Soul Foods Pink Morsel Dashboard

This project combines three supplied Soul Foods sales files, extracts Pink Morsel
transactions, calculates sales revenue, and presents the result in an interactive
Dash line chart with regional filtering.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python data_processor.py
python app.py
```

On Windows PowerShell, activate the environment with
`.venv\\Scripts\\Activate.ps1`.

## Tests

Run the browser tests through the CI helper:

```bash
./run_tests.sh
```

Google Chrome is required for the Dash browser tests.
