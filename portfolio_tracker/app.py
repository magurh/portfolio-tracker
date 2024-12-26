from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from portfolio_tracker.layout import (
    create_tab_layout,
    tab_style,
    tab_selected_style,
)
from portfolio_tracker.loader import DataLoader
from portfolio_tracker.manager import PortfolioManager
from portfolio_tracker.config import config

# Load data
data_loader = DataLoader(config.type1_path)
type1_data = data_loader.get_type1_data()

# Precompute data for Stocks
stock_manager = PortfolioManager(type1_data, asset_type="stock")
stock_realized_gains = stock_manager.stocks.generate_realized_gains_dataframe()
stock_portfolio_overview = stock_manager.get_portfolio_overview()
stock_owned_assets = stock_manager.stocks.get_owned_assets()
stock_current_values, stock_unrealized_gains = (
    stock_manager.stocks.fetch_current_values()
)

# Precompute data for Index Funds
index_fund_manager = PortfolioManager(type1_data, asset_type="index_fund")
index_fund_realized_gains = (
    index_fund_manager.stocks.generate_realized_gains_dataframe()
)
index_fund_portfolio_overview = index_fund_manager.get_portfolio_overview()
index_fund_owned_assets = index_fund_manager.stocks.get_owned_assets()
index_fund_current_values, index_fund_unrealized_gains = (
    index_fund_manager.stocks.fetch_current_values()
)

# Create Dash app
app = Dash(__name__)


# Define the layout
app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="stock",  # Default tab
            children=[
                dcc.Tab(
                    label="Stocks",
                    value="stock",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Index Funds",
                    value="index_fund",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
            ],
        ),
        html.Div(id="tab-content"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
)
def update_tab_content(tab_value):
    if tab_value == "stock":
        return create_tab_layout(
            stock_realized_gains,
            stock_portfolio_overview,
            stock_owned_assets,
            stock_current_values,
            stock_unrealized_gains,
        )
    elif tab_value == "index_fund":
        return create_tab_layout(
            index_fund_realized_gains,
            index_fund_portfolio_overview,
            index_fund_owned_assets,
            index_fund_current_values,
            index_fund_unrealized_gains,
        )


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
