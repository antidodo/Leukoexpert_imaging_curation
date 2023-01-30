import sys


def main():
    """
    get a folder of dicom files then anonmyse them and save them as nifti files pluss a json of the tags

    - origin_path: the path to the folder with the dicom files
    - target_path: the path to the folder where the nifti files and the json files should be saved
    - pseuodonym_csv_path: the path to the csv file with the pseudonymisation and name of the patient pluss the folder name
    - verbose(v/V): if true the program will print out the progress


    :return:
    """
    # get path from command line
    # or hardcode it
    #origin_path = sys.argv[1]
    #target_path = sys.argv[2]
    origion_path = "/"
    target_path = "/"

    if len(sys.argv) > 3:
        if sys.argv[3] == "V" or sys.argv[3] == "v":
            verbose = True
    else:
        verbose = False


if __name__ == '__main__':
    main()