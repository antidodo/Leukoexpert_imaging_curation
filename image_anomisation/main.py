import argparse


def main():
    """
    get a folder of dicom files then anonmyse them and save them as nifti files pluss a json of the tags

    - origin_path: the path to the folder with the dicom files
    - target_path: the path to the folder where the nifti files and the json files should be saved
    - pseuodonym_csv_path: the path to the csv file with the pseudonymisation and name of the patient pluss the folder name
    - verbose(v/V): if true the program will print out the progress


    :return:
    """
    parser = argparse.ArgumentParser(description='Curation of Mris')
    parser.add_argument('-o', type=str, help='the path to the origin folder', required=True)
    parser.add_argument('-t', type=str, help='the path to the target folder', required=True)
    parser.add_argument('-v', type=bool, help='verbose', default=False, required=False)


    args = parser.parse_args()
    origin_path = args.o
    target_path = args.t

    verbose = args.v
    print(origin_path)
    print(target_path)

    print(verbose)
if __name__ == '__main__':
    main()