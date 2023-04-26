import nibabel as nib
from nibabel.testing import data_path
import os
import numpy as np

def replace_descrip_nifty(input_path: str, output_path: str = None,pseudonym:str = None, inplace: bool = False, verbose: bool = False) -> [str,str]:
    """
    get a path to a nifty and change the descrip it. if inplace is true the original file will be overwritten
    :param input_path: the path to the nifty file
    :param output_path: the path to the output file
    :param pseudonym: the pseudonym to be used
    :param inplace: if true the original file will be overwritten
    :param verbose: if true the program will print out the progress
    :return: the old descrip and the new descrip
    """

    img = nib.load(input_path)
    if verbose:
        print(f" load file at: {input_path}")
    describe = img.header["descrip"]
    img.header["descrip"] = pseudonym
    if inplace:
        nib.save(img, input_path)
        if verbose:
            print(f" save file to path: {input_path}")
    else:
        if output_path is None:
            raise ValueError("output path is None, you need a output path if inplace is false")
        nib.save(img, output_path)
        if verbose:
            print(f" save file to path: {input_path}")
    return describe, pseudonym

def get_list_of_folders(path: str) -> list:
    """
    This function returns a list of all the folders in a given path.
    :param path:
    :return:
    """
    return [f.name for f in os.scandir(path) if f.is_dir()]

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
        os.mkdir(path)
