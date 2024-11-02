import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
from dash.dash_table import DataTable

# from portfolio_tracker.config import config

# Conditional colouring
column_band_mapping = [
    'pct_diff',
    'ref_vol',
]

style_data_conditional = []
for col in list(column_band_mapping.keys()):
    bands = column_band_mapping[col]  # Get the correct bands for the column
    for i, (bg_color, text_color) in enumerate(colors):
        low = 0 if i == 0 else bands[i-1]  # Lower bound is either 0 or the previous band
        high = bands[i] if i < len(bands) else float('inf')  # Upper bound is band[i] or infinity
        style_data_conditional.append({
            'if': {
                'filter_query': f'{{{col}}} >= {low} && {{{col}}} < {high}',
                'column_id': col
            },
            'backgroundColor': bg_color,
            'color': text_color
        })



app_layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Portfolio Tracker", className="text-center mb-4"
                ),
                width=12,
            )
        ),
        # Realized Gains Table
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.H4("Feed Table")),
                            dbc.CardBody(
                                DataTable(
                                    df_realized_gains.to_dict('records'),
                                    [
                                        {"name": i, "id": i} for i in df_realized_gains.columns
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
                                    style_data_conditional= style_data_conditional, 
                                    sort_action="native",
                                    sort_mode="multi",
                                    page_action="native",
                                    page_size=5,
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
    fluid=True,  # Use the fluid container for responsiveness
    className="p-4",  # Add padding for a cleaner look
)
