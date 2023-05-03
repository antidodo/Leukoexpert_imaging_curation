import os

def get_list_of_files(path: str) -> list:
    """
    This function returns a list of all the files in a given path.
    :param path:
    :return:
    """
    return [f.name for f in os.scandir(path) if f.is_file()]

def mkdir_when_not_existent(path: str) -> None:
    """
    This function creates a folder when it does not exist.
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
