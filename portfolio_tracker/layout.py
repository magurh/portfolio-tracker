import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import dcc, html
from dash.dash_table import DataTable
from plotly.graph_objects import Figure

def generate_style_data_conditional():
    """Generate conditional styles for the DataTable."""
    column_band_mapping = {
        "pct_diff": [0, 1, 2, 5, 10],  # Example bands for pct_diff
        "ref_vol": [0, 0.5, 1, 2, 3],  # Example bands for ref_vol
    }

    colors = [
        ("#FFDDC1", "#000000"),
        ("#FFC4A3", "#000000"),
        ("#FFAAA5", "#000000"),
        ("#FF8A80", "#FFFFFF"),
    ]

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


def create_portfolio_distribution_plot(
    owned_assets_dict: dict,
    current_stock_values: dict,
) -> Figure:
    portfolio_values = {
        stock: owned_assets_dict[stock] * current_stock_values[stock]
        for stock in owned_assets_dict
    }
    labels = list(portfolio_values.keys())
    sizes = list(portfolio_values.values())

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=sizes,
                textinfo="label+percent",
                hole=0.3,
            )
        ]
    )
    fig.update_layout(
        title="Stock Portfolio Distribution by Current Value",
        paper_bgcolor="#1e1e1e",  # Background of the figure
        plot_bgcolor="#1e1e1e",  # Background of the plot area
        font=dict(color="white"),  # Text color
    )
    return fig

def create_unrealized_gains_plot(
    unrealized_gains: dict,
) -> Figure:
    df = pd.DataFrame(list(unrealized_gains.items()), columns=["Stock", "Unrealized Gain"])
    fig = px.bar(df, x="Stock", y="Unrealized Gain", title="Unrealized Gains")
    fig.update_layout(
        paper_bgcolor="#1e1e1e",  # Background of the figure
        plot_bgcolor="#1e1e1e",  # Background of the plot area
        font=dict(color="white"),  # Text color
    )
    fig.update_traces(marker_color="blue", marker_line_color="black", marker_line_width=1)
    return fig


def create_layout(
    df_realized_gains: pd.DataFrame,
    portfolio_overview: pd.DataFrame,
    owned_assets_dict: dict,
    current_stock_values: dict,
    unrealized_gains_dict: dict,
):
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
            # Portfolio Distribution Plot
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Portfolio Distribution")),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="portfolio-distribution",
                                        figure=create_portfolio_distribution_plot(
                                            owned_assets_dict, current_stock_values
                                        ),
                                    )
                                ),
                            ],
                            className="shadow-sm mb-4",
                        ),
                        width=12,
                    ),
                ]
            ),
            # Unrealized Gains Plot
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Unrealized Gains")),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="unrealized-gains",
                                        figure=create_unrealized_gains_plot(
                                            unrealized_gains_dict
                                        ),
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
        ],
        fluid=True,
        className="p-4",
    )
