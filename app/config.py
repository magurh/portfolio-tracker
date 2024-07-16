import os

def get_data_folder_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, '..', 'data')
    return data_folder

# Manually set paths to data files
data_path = get_data_folder_path()

type1_PATH = os.path.join(data_path, 'type1.csv')
type2_PATH = os.path.join(data_path, 'type2.csv')
type3_PATH = os.path.join(data_path, 'type3.csv')
