import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dash_table import DataTable

# Styling configurations
column_band_mapping = {
    "pct_diff": [0, 1, 2, 5, 10],  # Example bands for pct_diff
    "ref_vol": [0, 0.5, 1, 2, 3],  # Example bands for ref_vol
}

colors = [
    ("#FFDDC1", "#000000"),  # Low bands (bg, text)
    ("#FFC4A3", "#000000"),
    ("#FFAAA5", "#000000"),
    ("#FF8A80", "#FFFFFF"),  # High bands
]


def generate_style_data_conditional() -> list:
    """Generate conditional styles for the DataTable."""
    style_data_conditional = []
    for col, bands in column_band_mapping.items():
        for i, (bg_color, text_color) in enumerate(colors):
            low = 0 if i == 0 else bands[i - 1]
            high = bands[i] if i < len(bands) else float("inf")
            style_data_conditional.append(
                {
                    "if": {
                        "filter_query": f"{{{col}}} >= {low} && {{{col}}} < {high}",
                        "column_id": col,
                    },
                    "backgroundColor": bg_color,
                    "color": text_color,
                }
            )
    return style_data_conditional


def create_layout(df_realized_gains: pd.DataFrame, portfolio_overview: pd.DataFrame):
    """Create the layout for the Dash app."""
    style_data_conditional = generate_style_data_conditional()

    return dbc.Container(
        [
            # Header
            dbc.Row(
                dbc.Col(
                    html.H1("Portfolio Tracker", className="text-center mb-4"),
                    width=12,
                )
            ),
            # Portfolio Overview Table
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Portfolio Overview")),
                                dbc.CardBody(
                                    DataTable(
                                        data=portfolio_overview.reset_index().to_dict("records"),
                                        columns=[
                                            {"name": "Metric", "id": "Metric"},
                                            {"name": "Stocks", "id": "Stocks"},
                                        ],
                                        id="portfolio-overview-table",
                                        style_table={"overflowX": "auto"},
                                        style_data={
                                            "backgroundColor": "rgb(50, 50, 50)",
                                            "color": "white",
                                        },
                                        style_cell={"textAlign": "center"},
                                        style_header={
                                            "fontWeight": "bold",
                                            "backgroundColor": "rgb(30, 30, 30)",
                                            "color": "white",
                                        },
                                    )
                                ),
                            ],
                            className="shadow-sm mb-4",
                        ),
                        width=12,
                    ),
                ]
            ),
            # Realized Gains Table
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Realized Gains")),
                                dbc.CardBody(
                                    DataTable(
                                        data=df_realized_gains.to_dict("records"),
                                        columns=[
                                            {"name": i, "id": i}
                                            for i in df_realized_gains.columns
                                        ],
                                        id="realized-gains-table",
                                        style_table={"overflowX": "auto"},
                                        style_data={
                                            "backgroundColor": "rgb(50, 50, 50)",
                                            "color": "white",
                                        },
                                        style_cell={"textAlign": "center"},
                                        style_header={
                                            "fontWeight": "bold",
                                            "backgroundColor": "rgb(30, 30, 30)",
                                            "color": "white",
                                        },
                                        style_data_conditional=style_data_conditional,
                                        sort_action="native",
                                        sort_mode="multi",
                                        page_action="native",
                                        page_size=20,
                                    )
                                ),
                            ],
                            className="shadow-sm mb-4",
                        ),
                        width=12,
                    ),
                ]
            ),
            # Interval component
            dcc.Interval(id="interval-component", interval=1 * 1000, n_intervals=0),
        ],
        fluid=True,
        className="p-4",
    )
