from portfolio_tracker.layout import create_layout
from portfolio_tracker.loader import DataLoader
from portfolio_tracker.manager import Stocks
from portfolio_tracker.config import config
from dash import Dash

# Load data
data_loader = DataLoader(config.type1_path)
type1_data = data_loader.get_type1_data()

# Process stock transactions
stocks = Stocks()
stocks.process_transactions(type1_data)

# Calculate gains
realized_gains_df = stocks.generate_realized_gains_dataframe()  # Move logic to `Stocks`

# Create Dash app
app = Dash(__name__)
app.layout = create_layout(realized_gains_df)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
