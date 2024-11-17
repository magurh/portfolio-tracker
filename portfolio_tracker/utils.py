import os


def get_data_folder_path(data_type: str = "public"):
    """
    Get data folder path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if data_type == "public":
        data_folder = os.path.join(current_dir, "..", "data")
    elif data_type == "private":
        data_folder = os.path.join(current_dir, "..", "data/personal_data")
    else:
        raise ValueError("Data type not supported.")

    return data_folder
