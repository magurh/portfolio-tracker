"""
There are 3 types of datasets:
1. type1: ['date', 'security', 'type_of_asset', 'action', 'quantity', 'total_transaction_price_usd']

This is the "fundamental type of dataset, which will be initially implemented in the portfolio tracker.

Future features will include crypto-currencies and commisions through:

2. type2: ['date', 'security_1', 'security_2', 'quantity_security_1', 'quantity_security_2']
3. type3: ['date', 'commission', 'amount']

"""

import numpy as np
import pandas as pd
import datetime
from portfolio_tracker.config import type1_df_path, type2_df_path, type3_df_path

CURRENT_DATE = datetime.datetime.now().date()


class DataLoader:
    """
    A class for loading the three types of datasets (if they exist in the data path).
    """
    def __init__(self, type1_path, type2_path=None, type3_path=None):
        self.type1_df = pd.read_csv(type1_path)
        self.type2_df = pd.read_csv(type2_path) if type2_path else None
        self.type3_df = pd.read_csv(type3_path) if type3_path else None

        # Convert columns to appropriate data types
        self._convert_types()

    def _convert_types(self):
        """
        Convert columns to appropriate data types and sort type1_df by date.
        """
        def clean_and_convert_to_float(series):
            # Ensure the series is a string, then remove commas and convert to float
            return series.astype(str).str.replace(',', '').astype(float)

        self.type1_df['quantity'] = clean_and_convert_to_float(self.type1_df['quantity'])
        self.type1_df['price_per_share'] = clean_and_convert_to_float(self.type1_df['price_per_share'])
        self.type1_df['total_transaction_price'] = clean_and_convert_to_float(self.type1_df['total_transaction_price'])
        self.type1_df['date'] = pd.to_datetime(self.type1_df['date'], format='%m/%d/%Y')

        # Sort by date
        self.type1_df.sort_values(by='date', inplace=True)


    def get_type1_data(self):
        return self.type1_df

    def get_type2_data(self):
        return self.type2_df

    def get_type3_data(self):
        return self.type3_df
