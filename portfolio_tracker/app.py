import yfinance as yf
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from adjustText import adjust_text

from portfolio_tracker.config import type1_PATH
from portfolio_tracker.manager import Stocks, PortfolioManager
from portfolio_tracker.loader import DataLoader
from portfolio_tracker.data_fetching import fetch_stock_prices, fetch_exchange_rate

from dash import dcc, html, dash_table, Dash

import plotly.express as px


# Load data
data_loader = DataLoader(type1_PATH)
type1_data = data_loader.get_type1_data()

# Process stock transactions and fetch current values
stocks = Stocks()
stocks.process_transactions(type1_data)

# Get realized and unrealized gains
owned_assets_dict = stocks.get_owned_assets()
current_stock_values, unrealized_gains_dict = stocks.fetch_current_values()
total_gains, realized_gains_dict = stocks.get_realized_gains()


data = []
for asset, gains_data in realized_gains_dict.items():
    realized_gains, total_sold_value, total_shares_sold, date_of_last_sell = gains_data
    data.append([asset, total_shares_sold, date_of_last_sell, total_sold_value, realized_gains])

df_realized_gains = pd.DataFrame(data, columns=["asset", "Shares sold", "Date last sell", "Total value sold", "Realized gains"])
df_realized_gains['Initial investment'] = df_realized_gains['Total value sold'] + df_realized_gains['Realized gains']
df_realized_gains['Rate of return (%)'] =  df_realized_gains['Realized gains']/df_realized_gains['Initial investment']*100 # excluding dividents
df_realized_gains = df_realized_gains[['asset', 'Initial investment', 'Shares sold', 'Total value sold', 'Date last sell', 'Realized gains', 'Rate of return (%)']]

# Format columns
columns_to_format = ['Realized gains', 'Rate of return (%)', 'Initial investment', 'Total value sold']
for column in columns_to_format:
    df_realized_gains[column] = df_realized_gains[column].apply(lambda x: f'{x:.2f}')
df_realized_gains['Date last sell'] = df_realized_gains['Date last sell'].dt.strftime('%d-%m-%Y')
# portfolio_manager = PortfolioManager(stock_transactions)


# Create a Dash app
app = Dash(__name__)

# Create a table using Plotly's DataTable component
app.layout = dash_table.DataTable(df_realized_gains.to_dict('records'), [{"name": i, "id": i} for i in df_realized_gains.columns])

    
#         id='realized-gains-table',
#         columns=[{'name': col, 'id': col} for col in df_realized_gains.columns],
#         data=df_realized_gains.to_dict('records'),
#         style_header={'backgroundColor': 'paleturquoise', 'color': 'black', 'textAlign': 'center'},
#         style_data={'backgroundColor': 'white', 'color': 'black'},
#         style_cell={'textAlign': 'center'},
#         pagination_mode='records',
#         pagination_settings={'current_page': 0, 'page_size': 10, 'total_records': len(df_realized_gains)}
#     )
# ])

# Layout for the Dash app
# app.layout = html.Div([
#     html.H1('Realized Gains Table'),
#     table
# ])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)