import argparse
import os
import pandas as pd
from utils_anomisation import get_list_of_folders , replace_descrip_nifty, mkdir_when_not_existent, get_list_of_files

def main():
    """
    get a folder of nifti

    - origin_path: the path to the folder with the dicom files
    - target_path: the path to the folder where the nifti files and the json files should be saved
    - pseuodonym_csv_path: the path to the csv file with the pseudonymisation and name of the patient pluss the folder name
    - verbose(v/V): if true the program will print out the progress


    :return:
    """
    parser = argparse.ArgumentParser(description='Curation of Mris')
    parser.add_argument('-o', type=str, help='the path to the origin folder', required=True)
    parser.add_argument('-t', type=str, help='the path to the target folder',default= None, required=False)
    parser.add_argument('-i',action='store_true' ,help='inplace')
    parser.add_argument('-v',action='store_true' ,help='verbose')


    args = parser.parse_args()
    origin_path = args.o
    target_path = args.t
    verbose = args.v
    inplace = args.i
    if verbose:
        print(f"origin_path: {origin_path}")
        print(f"target_path: {target_path}")
        print(f"inplace: {inplace}")
        print(f"verbose: {verbose}")
    # initilize a pandas dataframe for logging the changes made
    logs = pd.DataFrame(columns=["old_descrip", "pseudonym", "path"])

    # use the folder name as pseudonym
    list_of_pseudonym = get_list_of_folders(origin_path)
    # iterate of all the pseudonyms
    for pseudonym in list_of_pseudonym:
        path_of_imaging_dates = os.path.join(origin_path,pseudonym)
        list_of_imaging_dates = get_list_of_folders(path_of_imaging_dates)
        for imaging_date in list_of_imaging_dates:
            path_of_images = os.path.join(path_of_imaging_dates,imaging_date)

            list_of_images = get_list_of_files(path_of_images)

            for image in list_of_images:
                path_of_image = os.path.join(path_of_images,image)

                if inplace:
                    describe, pseudonym = replace_descrip_nifty(input_path = path_of_image,pseudonym = pseudonym , inplace = inplace, verbose = verbose)
                    logs = pd.concat([logs, pd.DataFrame(
                        [{"old_descrip": describe, "pseudonym": pseudonym, "path": path_of_image}])], ignore_index=True)
                else:
                    path_of_image_folder_target = os.path.join(target_path,pseudonym,imaging_date)
                    path_of_image_target = os.path.join(target_path,pseudonym,imaging_date,image)
                    mkdir_when_not_existent(path_of_image_folder_target)
                    describe, pseudonym = replace_descrip_nifty(input_path = path_of_image,output_path = path_of_image_target,pseudonym = pseudonym , inplace = inplace, verbose = verbose)
                    logs = pd.concat([logs, pd.DataFrame([{"old_descrip": describe, "pseudonym": pseudonym, "path": path_of_image_target}]) ], ignore_index=True)

    # save the logs
    logs.to_csv(os.path.join(origin_path,"Change_logs.csv"), index=False)
if __name__ == '__main__':
    main()