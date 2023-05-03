import os
import shutil


def copy_files(source_folder, target_folder):
    """Copy all files in subdirectories of source_folder to target_folder."""
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            src = os.path.join(root, filename)
            subfolder_name = root.split(source_folder)[1].replace("/", "&")
            new_filename = subfolder_name + "&" + filename
            dst = os.path.join(target_folder, new_filename)
            shutil.copyfile(src, dst)

            #shutil.copyfile(src, dst)


if __name__ == '__main__':
    source_folder = '/home/davidhieber/Documents/Leucoexpert/test_folder_mris/target/nifti/'
    target_folder = '/home/davidhieber/Documents/Leucoexpert/test_folder_mris/target/nifti_skull_stripped/'
    copy_files(source_folder, target_folder)