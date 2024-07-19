import numpy as np
import pandas as pd
import datetime
from app.config import type1_df_path, type2_df_path, type3_df_path

CURRENT_DATE = datetime.datetime.now().date()


class DataLoader:
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
