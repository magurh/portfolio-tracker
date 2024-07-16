import pandas as pd
import yfinance as yf
import cryptocompare
from forex_python.converter import CurrencyRates

from app.data_fetching import fetch_stock_price, fetch_crypto_price, fetch_exchange_rate


# Function to calculate account value
def calculate_account_value(type1_df):
    account_value_usd = type1_df['total_transaction_price_usd'].sum()
    exchange_rate = fetch_exchange_rate('GBP', 'USD')
    account_value_gbp = account_value_usd/exchange_rate
    return account_value_gbp, account_value_usd

# Function to calculate unrealized gains
def calculate_unrealized_gains(type1_df):
    unrealized_gains = 0
    for _, row in type1_df.iterrows():
        current_price = None
        if row['type_of_asset'] in ['Stock', 'Index Fund']:
            current_price = fetch_stock_price(row['security'])
        elif row['type_of_asset'] == 'Crypto':
            current_price = fetch_crypto_price(row['security'])
        
        if current_price is not None:
            if row['action'] == 'buy':
                unrealized_gains += (current_price - row['total_transaction_price_usd']) * row['quantity']
    
    return unrealized_gains

# Function to calculate realized gains
def calculate_realized_gains(type1_df):
    realized_gains = 0
    for _, row in type1_df.iterrows():
        if row['action'] == 'sell':
            initial_buy_price = type1_df[(type1_df['security'] == row['security']) & 
                                         (type1_df['action'] == 'buy')]['total_transaction_price_usd'].sum()
            realized_gains += (row['total_transaction_price_usd'] - initial_buy_price)
    return realized_gains

# Function to calculate day change (simplified)
def calculate_day_change(type1_df):
    day_change = 0
    for _, row in type1_df.iterrows():
        current_price = None
        if row['type_of_asset'] in ['Stock', 'Index Fund']:
            current_price = fetch_stock_price(row['security'])
        elif row['type_of_asset'] == 'Crypto':
            current_price = fetch_crypto_price(row['security'])
        
        if current_price is not None:
            day_change += (current_price - row['total_transaction_price_usd']) * row['quantity']
    return day_change

# Function to calculate dividend income
def calculate_dividend_income(type1_df):
    dividend_income = type1_df[type1_df['action'] == 'dividend']['total_transaction_price_usd'].sum()
    return dividend_income

# Function to calculate total commissions
def calculate_total_commissions(type3_df):
    total_commissions = type3_df['amount_usd'].sum()
    return total_commissions

# Function to calculate metrics for individual stocks, index funds, and crypto
def calculate_individual_metrics(type1_df, asset_type):
    filtered_df = type1_df[type1_df['type_of_asset'] == asset_type]
    
    account_value = filtered_df['total_transaction_price_usd'].sum()
    unrealized_gains = calculate_unrealized_gains(filtered_df)
    realized_gains = calculate_realized_gains(filtered_df)
    dividend_income = filtered_df[filtered_df['action'] == 'dividend']['total_transaction_price_usd'].sum()
    total_commissions = calculate_total_commissions(filtered_df)
    
    return {
        'account_value': account_value,
        'unrealized_gains': unrealized_gains,
        'realized_gains': realized_gains,
        'dividend_income': dividend_income,
        'total_commissions': total_commissions
    }

# Main calculation function
def calculate_portfolio_metrics(type1_df, type2_df, type3_df):
    account_value_gbp, account_value_usd = calculate_account_value(type1_df)
    unrealized_gains = calculate_unrealized_gains(type1_df)
    realized_gains = calculate_realized_gains(type1_df)
    day_change = calculate_day_change(type1_df)
    dividend_income = calculate_dividend_income(type1_df)
    total_commissions = calculate_total_commissions(type3_df)

    stock_metrics = calculate_individual_metrics(type1_df, 'Stock')
    index_fund_metrics = calculate_individual_metrics(type1_df, 'Index Fund')
    crypto_metrics = calculate_individual_metrics(type1_df, 'Crypto')
    
    metrics = {
        'account_value_gbp': account_value_gbp,
        'account_value_usd': account_value_usd,
        'unrealized_gains': unrealized_gains,
        'realized_gains': realized_gains,
        'day_change': day_change,
        'dividend_income': dividend_income,
        'total_commissions': total_commissions,
        'stock_metrics': stock_metrics,
        'index_fund_metrics': index_fund_metrics,
        'crypto_metrics': crypto_metrics
    }
    
    return metrics
