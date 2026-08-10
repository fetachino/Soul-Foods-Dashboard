"""Interactive Soul Foods dashboard for Pink Morsel sales."""

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

from data_processor import OUTPUT_FILE, build_sales_data


def load_sales_data(path: Path = OUTPUT_FILE) -> pd.DataFrame:
    """Load the formatted data, creating it from the raw inputs when necessary."""
    if not path.exists():
        build_sales_data(output_file=path)
    sales = pd.read_csv(path, parse_dates=["date"])
    return sales.sort_values("date", ignore_index=True)


sales_data = load_sales_data()
REGIONS = ["north", "east", "south", "west", "all"]

app = Dash(__name__)
server = app.server
app.title = "Soul Foods Pink Morsel Sales"


@server.get("/health")
def health():
    """Return a lightweight health response for deployment monitoring."""
    return {"status": "ok"}

app.layout = html.Main(
    className="dashboard",
    children=[
        html.Header(
            className="dashboard-header",
            children=[
                html.P("SOUL FOODS", className="eyebrow"),
                html.H1("Pink Morsel Sales Dashboard", id="dashboard-header"),
                html.P(
                    "Explore daily Pink Morsel revenue across every sales region.",
                    className="subtitle",
                ),
            ],
        ),
        html.Section(
            className="dashboard-card controls",
            children=[
                html.H2("Choose a region"),
                dcc.RadioItems(
                    id="region-picker",
                    options=[{"label": region, "value": region} for region in REGIONS],
                    value="all",
                    inline=True,
                    className="region-picker",
                    inputClassName="region-input",
                    labelClassName="region-label",
                ),
            ],
        ),
        html.Section(
            className="dashboard-card chart-card",
            children=dcc.Graph(id="sales-line-chart", config={"displayModeBar": False}),
        ),
    ],
)


@app.callback(Output("sales-line-chart", "figure"), Input("region-picker", "value"))
def update_chart(region: str):
    """Return a date-sorted sales line for the selected region or all regions."""
    filtered = sales_data if region == "all" else sales_data.loc[sales_data["region"] == region]
    daily_sales = filtered.groupby("date", as_index=False, sort=True)["sales"].sum()

    figure = px.line(
        daily_sales,
        x="date",
        y="sales",
        markers=True,
        labels={"date": "Date", "sales": "Sales ($)"},
        title=f"Pink Morsel Sales — {region.title()}",
    )
    figure.update_layout(
        template="plotly_white",
        margin={"l": 55, "r": 25, "t": 70, "b": 55},
        hovermode="x unified",
    )
    figure.update_traces(line={"color": "#d63384", "width": 3})
    return figure


if __name__ == "__main__":
    app.run(debug=True)
