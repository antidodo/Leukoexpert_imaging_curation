import os


def get_list_of_folders(path: str) -> list:
    """
    This function returns a list of all the folders in a given path.
    :param path:
    :return:
    """
    return [f.name for f in os.scandir(path) if f.is_dir()]


def mkdir_when_not_existent(path: str) -> None:
    """
    This function creates a folder when it does not exist.
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)


def make_list_of_dirs_in_path(path: str, names: list) -> None:
    """
    This function makes a dir for every name in the list of names at the given path.
    :param path:
    :return:
    """
    for name in names:
        mkdir_when_not_existent(path + name)


def get_path_of_a_file_in_a_folder(path: str, file_name: str) -> str or None:
    """
    This function returns the path of a file in a folder or a sub folder.
    :param path:
    :param file_name:
    :return:
    """
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def check_if_text_is_a_date_and_output_in_isofromat(date: str) -> str:
    """
    This function checks if a text is a date and outputs it in iso format.
    :param text:
    :return:
    """
    # remove all characters that are not numbers  from te sub folder name
    date_iso = date.replace(" ", "")
    date_iso = date_iso.replace("-", "")
    date_iso = date_iso.replace(":", "")
    date_iso = date_iso.replace(".", "")
    # check if record_date is numeric
    if not date_iso.isnumeric():
        print(f"date is not numeric  {date}")
        return ""
    # check if the recorde date is a valid date
    if not (1900 < int(date_iso[:4]) < 2100 and 1 <= int(date_iso[4:6]) <= 12 and 1 <= int(
            date_iso[6:8]) <= 31):
        print(f"not a valid date {date}")
        return ""
    # convert to iso formatted date
    date_iso = date_iso[:4] + "-" + date_iso[4:6] + "-" + date_iso[6:8]
    return date_iso
