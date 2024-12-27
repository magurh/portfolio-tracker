import dash_bootstrap_components as dbc
import pandas as pd

from dash import dcc, html
from dash.dash_table import DataTable
from plotly.graph_objects import Figure

from portfolio_tracker.config import config
from portfolio_tracker.plotter import (
    create_portfolio_distribution_plot,
    create_unrealized_gains_plot,
)

# Define style for tab buttons
tab_style = {
    "backgroundColor": config.colors.bg_color,
    "color": config.colors.txt_color,
    "padding": "10px",
    "border": "1px solid #444",
    "border-radius": "4px",
}

tab_selected_style = {
    **tab_style,
    "backgroundColor": "#444",  # Highlighted bg for the selected tab
    "border": "1px solid #888",  # Distinct border for active tab
    "fontWeight": "bold",  # Bold text for emphasis
}


def generate_style_data_conditional():
    """
    Generate conditional styles for the DataTable.
    Applies coloring based on positive/negative values in specific columns.
    """
    colors = [
        (config.colors.green_color, config.colors.txt_color),
        (config.colors.red_color, config.colors.txt_color),
    ]

    # Define the columns to apply conditional formatting
    columns_to_style = [
        "Realized gains",
        "Rate of return (%)",
    ]

    # Generate the style rules
    style_data_conditional = []
    for col in columns_to_style:
        # Rule for positive or zero values
        style_data_conditional.append(
            {
                "if": {
                    "filter_query": f"{{{col}}} >= 0",
                    "column_id": col,
                },
                "backgroundColor": colors[0][0],
                "color": colors[0][1],
            }
        )
        # Rule for negative values
        style_data_conditional.append(
            {
                "if": {
                    "filter_query": f"{{{col}}} < 0",
                    "column_id": col,
                },
                "backgroundColor": colors[1][0],
                "color": colors[1][1],
            }
        )

    return style_data_conditional


# Generate conditional style
style_data_conditional = generate_style_data_conditional()


def create_figure_card(
    title=str,
    card_id=str,
    figure=Figure,
) -> dbc.Card:
    """Creat a Dash Card for a Figure."""
    return dbc.Card(
        [
            dbc.CardHeader(html.H4(title)),
            dbc.CardBody(
                dcc.Graph(
                    id=card_id,
                    figure=figure,
                )
            ),
        ],
        className="shadow-sm mb-4",
    )


def create_tab_layout(
    df_realized_gains: pd.DataFrame,
    portfolio_overview: pd.DataFrame,
    owned_assets_dict: dict,
    current_stock_values: dict,
    unrealized_gains_dict: dict,
):
    """Create the layout for a single tab in the Dash app."""
    style_data_conditional = generate_style_data_conditional()

    return dbc.Container(
        [
            # Portfolio Overview Table
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Portfolio Overview")),
                                dbc.CardBody(
                                    DataTable(
                                        data=portfolio_overview.reset_index().to_dict(
                                            "records"
                                        ),
                                        columns=[
                                            {"name": "Metric", "id": "Metric"},
                                            {"name": "Value (USD)", "id": "Stocks"},
                                        ],
                                        id="portfolio-overview-table",
                                        style_table={"overflowX": "auto"},
                                        style_data={
                                            "backgroundColor": "rgb(50, 50, 50)",
                                            "color": config.colors.txt_color,
                                        },
                                        style_cell={"textAlign": "center"},
                                        style_header={
                                            "fontWeight": "bold",
                                            "backgroundColor": "rgb(30, 30, 30)",
                                            "color": config.colors.txt_color,
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
                        create_figure_card(
                            title="Portfolio Distribution",
                            card_id="portfolio-distribution",
                            figure=create_portfolio_distribution_plot(
                                owned_assets_dict, current_stock_values
                            ),
                        ),
                        width=12,
                    ),
                ]
            ),
            # Unrealized Gains Plot
            dbc.Row(
                [
                    dbc.Col(
                        create_figure_card(
                            title="Unrealized Gains",
                            card_id="unrealized-gains",
                            figure=create_unrealized_gains_plot(unrealized_gains_dict),
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
                                            "color": config.colors.txt_color,
                                        },
                                        style_cell={"textAlign": "center"},
                                        style_header={
                                            "fontWeight": "bold",
                                            "backgroundColor": "rgb(30, 30, 30)",
                                            "color": config.colors.txt_color,
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
            # Spacer Row
            dbc.Row(
                html.Div(style={"height": "100px"}),
            ),
        ],
        fluid=True,
        className="p-4",
    )
