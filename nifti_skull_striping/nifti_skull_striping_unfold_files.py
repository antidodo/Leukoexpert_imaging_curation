import os
from utils_nifti_skull_striping import get_list_of_files , mkdir_when_not_existent
import shutil


def copy_files(source_folder, target_folder):
    """copy files with ending _bet.nii to target_folder. copy into subfolder with name of parent folder."""
    # get list of files in source_folder
    list_of_files = get_list_of_files(source_folder)
    # iterate over list of files
    for file in list_of_files:
        # check if file ends with _bet.nii
        if not file.endswith("_bet.nii"):
            continue
        # split file into name and original path
        split_file_name = file.split("&")
        file_name = split_file_name[-1]
        original_path = split_file_name[:-1]
        original_path = "/".join(original_path)
        # create new path
        new_path = os.path.join(target_folder, original_path)
        mkdir_when_not_existent(new_path)
        # copy file to new path
        src = os.path.join(source_folder, file)
        dec = os.path.join(new_path, file_name)
        shutil.copyfile(src, dec)

if __name__ == '__main__':
    source_folder = '/home/davidhieber/Documents/Leucoexpert/test_folder_mris/target/nifti_skull_stripped/'
    target_folder = '/home/davidhieber/Documents/Leucoexpert/test_folder_mris/target/reconstitutet/'
    copy_files(source_folder, target_folder)