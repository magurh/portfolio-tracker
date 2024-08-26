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

    def get_type1_data(self):
        return self.type1_df

    def get_type2_data(self):
        return self.type2_df

    def get_type3_data(self):
        return self.type3_df
