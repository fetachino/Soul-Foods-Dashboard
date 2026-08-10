"""Build the Pink Morsel sales dataset from the three supplied CSV files."""

from pathlib import Path

import pandas as pd


REPOSITORY_DIR = Path(__file__).resolve().parent
DATA_DIR = REPOSITORY_DIR / "data"
OUTPUT_FILE = DATA_DIR / "formatted_sales_data.csv"


def build_sales_data(data_dir: Path = DATA_DIR, output_file: Path = OUTPUT_FILE) -> pd.DataFrame:
    """Combine the raw files, calculate Pink Morsel sales, and save the result."""
    input_files = sorted(data_dir.glob("daily_sales_data_*.csv"))
    if len(input_files) != 3:
        raise FileNotFoundError(
            f"Expected three daily sales CSV files in {data_dir}, found {len(input_files)}."
        )

    combined = pd.concat((pd.read_csv(path) for path in input_files), ignore_index=True)
    pink_morsels = combined.loc[
        combined["product"].astype(str).str.strip().str.casefold() == "pink morsel"
    ].copy()

    prices = pd.to_numeric(
        pink_morsels["price"].astype(str).str.replace("$", "", regex=False),
        errors="raise",
    )
    quantities = pd.to_numeric(pink_morsels["quantity"], errors="raise")
    pink_morsels["sales"] = quantities * prices
    pink_morsels["date"] = pd.to_datetime(pink_morsels["date"], errors="raise")
    pink_morsels["region"] = pink_morsels["region"].astype(str).str.strip().str.casefold()

    result = pink_morsels.loc[:, ["sales", "date", "region"]].sort_values(
        ["date", "region"], ignore_index=True
    )
    result.to_csv(output_file, index=False, date_format="%Y-%m-%d")
    return result


if __name__ == "__main__":
    rows = build_sales_data()
    print(f"Wrote {len(rows)} Pink Morsel sales rows to {OUTPUT_FILE}")
