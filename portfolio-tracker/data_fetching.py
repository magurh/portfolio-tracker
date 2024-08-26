import ffn
import yfinance as yf
from app.config import crypto_exchange_map
import ccxt
import requests
# from forex_python.converter import CurrencyRates
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



def fetch_stock_prices(symbols, currency='USD'):
    """
    Fetches the current prices of multiple stocks or index funds.

    Parameters:
    - symbols: List of ticker symbols of the stocks/index funds (e.g., ['AAPL', 'MSFT'])
    - currency: Currency to convert to ('USD' or 'GBP')

    Returns:
    - Dictionary where keys are symbols and values are current prices in the specified currency.
    """
    prices = {}
    tickers = yf.Tickers(' '.join(symbols))
    exchange_rate = fetch_exchange_rate('USD', 'GBP') if currency == 'GBP' else 1

    for symbol in symbols:
        ticker = tickers.tickers[symbol]
        data = ticker.history(period='1d')
        if not data.empty:
            price = data['Close'].iloc[-1] * exchange_rate
            prices[symbol] = price

    return prices


def fetch_crypto_price(symbol, currency='USD'):
    """
    Fetches the current price of a cryptocurrency.

    Parameters:
    - symbol: Ticker symbol of the cryptocurrency (e.g., 'BTC' for Bitcoin)
    - currency: Currency to convert to ('USD' or 'GBP')

    Returns:
    - Current price of the cryptocurrency in the specified currency.
    """
    exchange_name = crypto_exchange_map.get(symbol, 'binance')
    exchange = getattr(ccxt, exchange_name)()
    ticker = exchange.fetch_ticker(symbol + '/USDT')
    price = ticker['last']

    return price if currency == 'USD' else price * fetch_exchange_rate('USD', currency)

