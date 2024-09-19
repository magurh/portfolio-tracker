"""
Latest updates: 03/Aug/24
    - Stocks class: Process transactions and update the owned shares dictionary.
    - PortfolioManager class: current_portfolio_value, stock_percentage_of_portfolio
    
"""

import pandas as pd
from collections import deque
from portfolio_tracker.data_fetching import fetch_stock_prices, fetch_exchange_rate


class Stocks:
    def __init__(self):
        # Dictionary to track owned shares for each stock, where each stock maps to a deque of lots
        self.owned_shares = {}
        # Track total realized gains and gains per asset
        self.realized_gains = 0
        self.realized_gains_per_asset = {}
        # Track unrealized gains per asset
        self.unrealized_gains_per_asset = {}
        # Initialize exchange rates
        self.exchange_rates =  {}

    
    def process_transactions(self, transactions):
        """
        Process transactions and update the owned shares dictionary.

        Parameters:
        - transactions (DataFrame): DataFrame containing transactional data with columns:
            - 'date': Date of the transaction
            - 'security': Name of the security (e.g., 'TSLA')
            - 'type_of_asset': Type of asset ('stock', 'crypto', 'index_fund' etc.)
            - 'action': Action of the transaction ('buy' or 'sell')
            - 'quantity': Number of shares involved in the transaction
            - 'total_transaction_price_usd': Total transaction price in USD at the time of transaction
        """
        # Extract currencies and fetch exchange rates
        currencies = transactions['currency'].unique()
        
        earliest_dates = {}
        for currency in currencies:
            if currency != 'USD':
                earliest_date = transactions[transactions['currency'] == currency]['date'].min()
                earliest_dates[currency] = earliest_date

        end_date = pd.Timestamp.now().strftime('%Y-%m-%d')  # Current date
        for currency, earliest_date in earliest_dates.items():
            self.exchange_rates[currency] = fetch_exchange_rate(currency, 'USD', earliest_date, end_date)
                
        
        for _, transaction in transactions.iterrows():
            security = transaction['security']
            action = transaction['action']
            quantity = transaction['quantity']
            total_price = transaction['total_transaction_price']
            price_per_share = transaction['price_per_share']
            currency = transaction['currency']
            date = transaction['date']

            if currency != 'USD':
                exchange_rate = self.exchange_rates[currency].loc[date.strftime('%m/%d/%Y'), 'exchange_rate']
                if pd.isna(exchange_rate):
                    raise ValueError(f"Exchange rate not available for {currency} on {date}")
                price_per_share = price_per_share*exchange_rate
                total_price = total_price*exchange_rate


                
            if security not in self.owned_shares:
                self.owned_shares[security] = deque()
            
            if action == 'buy':
                # Add the new purchase as a lot to the deque for this security
                self.owned_shares[security].append((quantity, price_per_share))
            elif action == 'sell':
                self._sell_shares(security, quantity, price_per_share, date)

            # Remove the security from owned_shares if the total quantity is zero
            if sum(quantity for quantity, _ in self.owned_shares[security]) <= 0:
                del self.owned_shares[security]
    
    def _sell_shares(self, security, quantity, selling_price, transaction_date):
        """
        Helper function to sell shares using the FIFO method and update realized gains.
        
        Parameters:
        - security: The stock being sold.
        - quantity: The number of shares being sold.
        - selling_price: The price at which the shares are being sold.
        - transaction_date
        """
        if security not in self.owned_shares or sum(q for q, _ in self.owned_shares[security]) < quantity:
            raise ValueError(f"Not enough shares of {security} to sell {quantity}")
        
        remaining_quantity = quantity
        
        while remaining_quantity > 0:
            lot_quantity, lot_price = self.owned_shares[security][0]
            if lot_quantity > remaining_quantity:
                realized_gain = remaining_quantity * (selling_price - lot_price)
                self.realized_gains += realized_gain
                if security not in self.realized_gains_per_asset:
                    self.realized_gains_per_asset[security] = [0, 0, 0, 0] # (realized_gains, total_sold_value, total_shares_sold, date_of_last_sell) # 0 

                # Updates self.realized_gains_per_asset dictionary
                self.realized_gains_per_asset[security][0] += realized_gain
                        
                self.owned_shares[security][0] = (lot_quantity - remaining_quantity, lot_price)
                remaining_quantity = 0
            else:
                realized_gain = lot_quantity * (selling_price - lot_price)
                self.realized_gains += realized_gain
                if security not in self.realized_gains_per_asset:
                    self.realized_gains_per_asset[security] = [0, 0, 0, 0] # (realized_gains, total_sold_value, total_shares_sold, date_of_last_sell)  # 0 
                self.realized_gains_per_asset[security][0] += realized_gain
                remaining_quantity -= lot_quantity
                self.owned_shares[security].popleft()

        self.realized_gains_per_asset[security][1] += quantity*selling_price
        self.realized_gains_per_asset[security][2] += quantity
        self.realized_gains_per_asset[security][3] = transaction_date
    
    def get_owned_assets(self):
        """
        Get the current number of shares owned for each stock.

        Returns:
        - owned_assets (dict): A dictionary where keys are stock names and values are total number of shares owned.
        """
        owned_assets = {security: sum(quantity for quantity, _ in lots) 
                        for security, lots in self.owned_shares.items()}
        
        return owned_assets
    
    def fetch_current_values(self):
        """
        Fetch the current values and unrealized gains of the stocks currently owned.

        Returns:
        - current_values (dict): A dictionary where keys are stock names and values are current values in USD.
        - unrealized_gains (dict): A dictionary where keys are stock names and values are unrealized gains in USD.
        """
        owned_assets = self.get_owned_assets()
        symbols = list(owned_assets.keys())
        
        # Fetch current prices of owned stocks
        current_prices = fetch_stock_prices(symbols)
        
        # Calculate current values and unrealized gains
        current_values = {}
        self.unrealized_gains_per_asset = {}
        for symbol, shares in owned_assets.items():
            current_value = shares * current_prices.get(symbol, 0)
            current_values[symbol] = current_value
            
            # Calculate unrealized gains
            total_cost_basis = sum(quantity * price for quantity, price in self.owned_shares[symbol])
            unrealized_gain = current_value - total_cost_basis
            self.unrealized_gains_per_asset[symbol] = unrealized_gain
        
        return current_values, self.unrealized_gains_per_asset
    
    def get_realized_gains(self):
        """
        Get the total realized gains and realized gains per asset.

        Returns:
        - realized_gains (float): Total realized gains across all assets.
        - realized_gains_per_asset (dict): A dictionary where keys are stock names and values are realized gains in USD.
        """
        return self.realized_gains, self.realized_gains_per_asset



class PortfolioManager:
    def __init__(self, transactions, asset_type: str):
        self.transactions = transactions
        self.stocks = Stocks()
        self.stocks.process_transactions(self.transactions[(self.transactions['type_of_asset'] == 'stock') | (self.transactions['type_of_asset'] == 'index_fund')])
        self._current_values = None
    
    def _update_current_values(self):
        """
        Update the current values of the stocks and store them in an internal attribute.
        """
        self._current_values = self.stocks.fetch_current_values()[0]
    
    def current_portfolio_value(self):
        """
        Calculate the current value of the portfolio.

        Returns:
        - total_value (float): The total current value of the portfolio in USD.
        """
        if self._current_values is None:
            self._update_current_values()
        
        total_value = sum(self._current_values.values())
        return total_value
    
    def stock_percentage_of_portfolio(self):
        """
        Calculate the percentage of each stock in the total portfolio.

        Returns:
        - stock_percentages (dict): A dictionary where keys are stock names and values are their percentage of the total portfolio.
        """
        if self._current_values is None:
            self._update_current_values()
        
        total_value = self.current_portfolio_value()
        
        stock_percentages = {}
        for symbol, value in self._current_values.items():
            stock_percentages[symbol] = (value / total_value) * 100 if total_value != 0 else 0
        
        return stock_percentages