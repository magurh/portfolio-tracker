import os


def get_data_folder_path(data_type: str = "public"):
    """
    Get the folder path for storing datasets.

    :param data_type: 'public' for shared datasets, 'private' for personal data.
    :return: data folder path
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if data_type == "public":
        data_folder = os.path.join(current_dir, "..", "data")
    elif data_type == "private":
        data_folder = os.path.join(current_dir, "..", "data/personal_data")
    else:
        raise ValueError("Data type not supported.")

    return os.path.abspath(data_folder)
