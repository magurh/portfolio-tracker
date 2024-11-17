import pandas as pd

import yfinance as yf
from portfolio_tracker.config import config
import ccxt
# from forex_python.converter import CurrencyRates


def fetch_exchange_rate(base_currency, target_currency, start_date, end_date):
    """
    Fetches the exchange rates between two currencies for a specific date range.

    Parameters:
    - base_currency: Base currency code (e.g., 'USD')
    - target_currency: Target currency code (e.g., 'GBP')
    - start_date: Start date for the data (YYYY-MM-DD)
    - end_date: End date for the data (YYYY-MM-DD)

    Returns:
    - DataFrame with exchange rates and dates formatted as '%m/%d/%Y'.
    """
    ticker = f"{base_currency}{target_currency}=X"
    data = yf.Ticker(ticker)

    # Fetch data with a slightly larger range to ensure start_date is included
    fetch_start_date = pd.to_datetime(start_date) - pd.DateOffset(days=5)
    fetch_end_date = pd.to_datetime(end_date) + pd.DateOffset(days=5)

    hist = data.history(start=fetch_start_date, end=fetch_end_date)

    if not hist.empty:
        # Reset index to have 'Date' as a column
        hist_reset = hist[["Close"]].reset_index()

        # Format the 'Date' column
        hist_reset["Date"] = hist_reset["Date"].dt.strftime("%m/%d/%Y")
        hist_reset = hist_reset.rename(columns={"Close": "exchange_rate"})

        # Set the formatted date column as the index
        hist_reset = hist_reset[["Date", "exchange_rate"]]
        hist_reset.set_index("Date", inplace=True)

        # Ensure the DataFrame includes all dates from start_date to end_date
        all_dates = pd.date_range(start=start_date, end=end_date).strftime("%m/%d/%Y")
        full_df = pd.DataFrame(index=all_dates)
        full_df = full_df.join(hist_reset, how="left")

        # Fill in missing values
        full_df["exchange_rate"] = full_df["exchange_rate"].ffill()  # Forward fill
        full_df["exchange_rate"] = full_df["exchange_rate"].bfill()  # Backward fill

        return full_df
    else:
        # Return an empty DataFrame with the correct columns if no data was fetched
        all_dates = pd.date_range(start=start_date, end=end_date).strftime("%m/%d/%Y")
        full_df = pd.DataFrame(index=all_dates, columns=["exchange_rate"])
        return full_df


### BUG: currency change for the below functions


def fetch_stock_prices(symbols, currency="USD"):
    """
    Fetches the current prices of multiple stocks or index funds.

    Parameters:
    - symbols: List of ticker symbols of the stocks/index funds (e.g., ['AAPL', 'MSFT'])
    - currency: Currency to convert to ('USD' or 'GBP')

    Returns:
    - Dictionary where keys are symbols and values are current prices in the specified currency.
    """
    prices = {}
    tickers = yf.Tickers(" ".join(symbols))
    exchange_rate = fetch_exchange_rate("USD", "GBP") if currency == "GBP" else 1

    for symbol in symbols:
        ticker = tickers.tickers[symbol]
        data = ticker.history(period="1d")
        if not data.empty:
            price = data["Close"].iloc[-1] * exchange_rate
            prices[symbol] = price

    return prices


def fetch_crypto_price(symbol, currency="USD"):
    """
    Fetches the current price of a cryptocurrency.

    Parameters:
    - symbol: Ticker symbol of the cryptocurrency (e.g., 'BTC' for Bitcoin)
    - currency: Currency to convert to ('USD' or 'GBP')

    Returns:
    - Current price of the cryptocurrency in the specified currency.
    """
    exchange_name = config.crypto_exchange_map.get(symbol, "binance")
    exchange = getattr(ccxt, exchange_name)()
    ticker = exchange.fetch_ticker(symbol + "/USDT")
    price = ticker["last"]

    return price if currency == "USD" else price * fetch_exchange_rate("USD", currency)
