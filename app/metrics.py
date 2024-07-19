import pandas as pd
from app.data_fetching import fetch_stock_prices, fetch_exchange_rate
from app.loader import DataLoader

class Stocks:
    def __init__(self):
        self.owned_shares = {}  # Dictionary to track owned shares for each stock
    
    def process_transactions(self, transactions):
        """
        Process transactions and update the owned shares dictionary.

        Parameters:
        - transactions (DataFrame): DataFrame containing transactional data with columns:
            - 'date': Date of the transaction
            - 'security': Name of the security (e.g., 'TSLA')
            - 'type_of_asset': Type of asset ('Stock', 'Crypto', etc.)
            - 'action': Action of the transaction ('buy' or 'sell')
            - 'quantity': Number of shares involved in the transaction
            - 'total_transaction_price_usd': Total transaction price in USD at the time of transaction
        """
        for _, transaction in transactions.iterrows():
            security = transaction['security']
            action = transaction['action']
            quantity = transaction['quantity']
            
            if security not in self.owned_shares:
                self.owned_shares[security] = 0
            
            if action == 'buy':
                self.owned_shares[security] += quantity
            elif action == 'sell':
                if self.owned_shares[security] >= quantity:
                    self.owned_shares[security] -= quantity
                else:
                    raise ValueError(f"Not enough shares of {security} to sell {quantity}")
            else:
                raise ValueError(f"Invalid action: {action}")
    
    def get_owned_assets(self):
        """
        Get the current number of shares owned for each stock.

        Returns:
        - owned_assets (dict): A dictionary where keys are stock names and values are number of shares owned.
        """
        return self.owned_shares
    
    def fetch_current_values(self):
        """
        Fetch the current values of the stocks currently owned.

        Returns:
        - current_values (dict): A dictionary where keys are stock names and values are current values in USD.
        """
        owned_assets = self.get_owned_assets()
        symbols = list(owned_assets.keys())
        
        # Fetch current prices of owned stocks
        current_prices = fetch_stock_prices(symbols)
        
        # Calculate current values
        current_values = {}
        for symbol, shares in owned_assets.items():
            current_values[symbol] = shares * current_prices.get(symbol, 0)
        
        return current_values