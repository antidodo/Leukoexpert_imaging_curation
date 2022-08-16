import os

def get_list_of_folders(path: str) -> list:
    """
    This function returns a list of all the folders in a given path.
    :param path:
    :return:
    """
    return [f.name for f in os.scandir(path) if f.is_dir()]

