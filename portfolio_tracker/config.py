import os
from dataclasses import dataclass
from pathlib import Path

from portfolio_tracker.utils import get_data_folder_path


@dataclass(frozen=True, kw_only=True)
class Config:
    data_path: Path
    crypto_exchange_map: dict
    type1_path: Path
    type2_path: Path
    type3_path: Path


# Use private data -- for public data, i.e. data within the data folder, set data_type to 'public'
DATA_PATH = get_data_folder_path(data_type="private")

type1_PATH = os.path.join(DATA_PATH, "type1.csv")
type2_PATH = os.path.join(DATA_PATH, "type2.csv")
type3_PATH = os.path.join(DATA_PATH, "type3.csv")


# Dictionary to map cryptocurrencies to specific exchanges
EXCHANGE_MAP = {"BTC": "binance", "ETH": "binance", "LTC": "binance", "ADA": "binance"}


# Overwrite config as an instance of AppConfig
config = Config(
    data_path=DATA_PATH,
    type1_path=os.path.join(DATA_PATH, "type1.csv"),
    type2_path=os.path.join(DATA_PATH, "type2.csv"),
    type3_path=os.path.join(DATA_PATH, "type3.csv"),
    crypto_exchange_map=EXCHANGE_MAP,
)
