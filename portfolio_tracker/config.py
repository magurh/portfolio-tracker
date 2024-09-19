import os

def get_data_folder_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, '..', 'data/personal_data')
    return data_folder


DATA_PATH = get_data_folder_path()

type1_PATH = os.path.join(DATA_PATH, 'type1.csv')
type2_PATH = os.path.join(DATA_PATH, 'type2.csv')
type3_PATH = os.path.join(DATA_PATH, 'type3.csv')


# Dictionary to map cryptocurrencies to specific exchanges
crypto_exchange_map = {
    'BTC': 'binance',
    'ETH': 'binance',
    'LTC': 'binance',
    'ADA': 'binance'
}