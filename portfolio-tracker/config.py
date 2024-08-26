import os

def get_data_folder_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, '..', 'data')
    return data_folder

# Manually set paths to data files
data_path = get_data_folder_path()

type1_df_path = os.path.join(data_path, 'type1.csv')
type2_df_path = os.path.join(data_path, 'type2.csv')
type3_df_path = os.path.join(data_path, 'type3.csv')


# Dictionary to map cryptocurrencies to specific exchanges
crypto_exchange_map = {
    'BTC': 'binance',
    'ETH': 'binance',
    'LTC': 'binance',
    'ADA': 'binance'
}