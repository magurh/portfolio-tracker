import yfinance as yf
import cryptocompare
from forex_python.converter import CurrencyRates

import requests


def fetch_exchange_rate(base_currency, target_currency):
    """
    Fetches the exchange rate between two currencies.

    Parameters:
    - base_currency: Base currency code (e.g., 'USD')
    - target_currency: Target currency code (e.g., 'GBP')

    Returns:
    - Exchange rate from base_currency to target_currency.
    """
    ticker = f"{base_currency}{target_currency}=X"
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    if not hist.empty:
        return hist['Close'][0]
    else:
        return None


# Initialize CurrencyRates object for fetching exchange rates
# currency_converter = CurrencyRates()

def fetch_stock_price(symbol, currency='USD'):
    """
    Fetches the current price of a stock or index fund.

    Parameters:
    - symbol: Ticker symbol of the stock/index fund (e.g., 'AAPL' for Apple)
    - currency: Currency to convert to ('USD' or 'GBP')

    Returns:
    - Current price of the stock/index fund in the specified currency.
    """
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='1d')
    if not data.empty:
        if currency == 'GBP':
            return data['Close'][0] * fetch_exchange_rate('USD', 'GBP')
        else:
            return data['Close'][0]
    else:
        return None


def fetch_crypto_price(symbol, currency='USD'):
    """
    Fetches the current price of a cryptocurrency.

    Parameters:
    - symbol: Ticker symbol of the cryptocurrency (e.g., 'BTC' for Bitcoin)
    - currency: Currency to convert to ('USD' or 'GBP')

    Returns:
    - Current price of the cryptocurrency in the specified currency.
    """
    if currency == 'GBP':
        return cryptocompare.get_price(symbol, currency='GBP')[symbol]['GBP']
    else:
        return cryptocompare.get_price(symbol, currency='USD')[symbol]['USD']
