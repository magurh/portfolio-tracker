from portfolio_tracker.layout import create_layout
from portfolio_tracker.loader import DataLoader
from portfolio_tracker.manager import PortfolioManager
from portfolio_tracker.config import config
from dash import Dash, Input, Output

# Load data
data_loader = DataLoader(config.type1_path)
type1_data = data_loader.get_type1_data()

# Process stock transactions
portfolio_manager = PortfolioManager(type1_data, asset_type="stock")
realized_gains_df = portfolio_manager.stocks.generate_realized_gains_dataframe()  
portfolio_overview = portfolio_manager.get_portfolio_overview()

# Fetch current portfolio details
owned_assets_dict = portfolio_manager.stocks.get_owned_assets()
current_stock_values, unrealized_gains_dict = portfolio_manager.stocks.fetch_current_values()


# Create Dash app
app = Dash(__name__) #, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"])
app.layout = create_layout(
    realized_gains_df,
    portfolio_overview,
    owned_assets_dict,
    current_stock_values,
    unrealized_gains_dict,
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
