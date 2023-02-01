import sys
import csv

from utils import get_list_of_folders, mkdir_when_not_existent, make_list_of_dirs_in_path, \
    check_if_text_is_a_date_and_output_in_isofromat, get_path_of_a_file_in_a_folder, create_string_with_fill_zeros
import os


def main():
    """
    kuriert ->  dicom(ids(ios_datum(DICOM)))  , Niff(ids(iso_daum(Alle relvanten niffty)

    Main function for the data curation skript.
    At a spesifite path it creates tow sub folders Dicom and nif
    in both folders it creates the same folder with  names from an origin folder
    Then for every created folder it locks in the origin if ther a sub folders with dates as names
    it this is the case it copies the sub folder to the new renamed with iso formateded date as file name
    if ther is a dicom folder in the date folder from the orign folder it copies the dicom folder to the new folder
    same proces is repeated fo the niff folder, but only select secenses get copied
    :return:
    """
    # get the path from the args
    origin_path = sys.argv[1]
    target_path = sys.argv[2]

    pseudonymisation = True
    if len(sys.argv) > 3:
        if sys.argv[3] == "V" or sys.argv[3] == "v":
            verbose = True
    else:
        verbose = False

    if os.name == "nt":
        if not "\\\\" in origin_path:
            origin_path = origin_path.replace("\\","\\\\")
        if not "\\\\" in target_path:
            target_path = target_path.replace("\\","\\\\")
        # create the target path if they do not exist
        mkdir_when_not_existent(target_path)
        # create the dicom and nifti folder in the target folder if they do not exist
        mkdir_when_not_existent(target_path + r"\\dicom")
        mkdir_when_not_existent(target_path + r"\\nifti")
        patient_folders = get_list_of_folders(origin_path)


    else:
        # create the target path if they do not exist
        mkdir_when_not_existent(target_path)
        # create the dicom and nifti folder in the target folder if they do not exist
        mkdir_when_not_existent(target_path + "/dicom")
        mkdir_when_not_existent(target_path + "/nifti")
        patient_folders = get_list_of_folders(origin_path)



    patient_folders_and_pseudonyms = []
    if pseudonymisation:
        # create a list of patient folders and pseudonym numbers, the pseudonym number is the same as the index of the list

        pseudonym_number = 0
        for patient_folder  in patient_folders:

            pseudonym = create_string_with_fill_zeros(pseudonym_number, 5)

            patient_folders_and_pseudonyms.append([patient_folder,pseudonym])
            pseudonym_number += 1
    else:
        # patient folders and pseudonyms are the same
        patient_folders_and_pseudonyms = []
        for patient_folder in patient_folders:
            patient_folders_and_pseudonyms.append([patient_folder, patient_folder])
    pseudonyms_folders = [patient_folder_and_pseudonym[1] for patient_folder_and_pseudonym in patient_folders_and_pseudonyms]
    if os.name == "nt":
        # create the same folders in the target folder if they do not exist
        make_list_of_dirs_in_path(target_path + r"\\dicom\\", pseudonyms_folders)
        make_list_of_dirs_in_path(target_path + r"\\nifti\\", pseudonyms_folders)
        if verbose:
            print(f"patient folders created {patient_folders}")
    else:
        # create the same folders in the target folder if they do not exist
        make_list_of_dirs_in_path(target_path + "/dicom/", pseudonyms_folders)
        make_list_of_dirs_in_path(target_path + "/nifti/", pseudonyms_folders)
        if verbose:
            print(f"patient folders created {patient_folders_and_pseudonyms}")


    number_dicoms = 0
    # for every patient folder in the origin folder get the list of sub folder names, create a list of iso formatted dates
    for patient_folder_and_pseudonym in patient_folders_and_pseudonyms:
        patient_folder = patient_folder_and_pseudonym[0]
        pseudonym_number = patient_folder_and_pseudonym[1]
        if os.name == "nt":
            record_dates = get_list_of_folders(origin_path + r"\\" + patient_folder)
        else:
            record_dates = get_list_of_folders(origin_path + "/" + patient_folder)
        for record_date in record_dates:
            # check if the recorde date containes a dicom study
            dicom_folder_name = ""
            dicom_folder_name_options = ["dicom", "DICOM", "Dicom"]
            if os.name == "nt":
                for dicom_folder_name_option in dicom_folder_name_options:
                    if os.path.isdir(
                            origin_path + r"\\" + patient_folder + r"\\" + record_date + r"\\" + dicom_folder_name_option):
                        dicom_folder_name = dicom_folder_name_option
                        break
                if dicom_folder_name == "":
                    continue
            else:
                for dicom_folder_name_option in dicom_folder_name_options:
                    if os.path.isdir(
                            origin_path + "/" + patient_folder + "/" + record_date + "/" + dicom_folder_name_option):
                        dicom_folder_name = dicom_folder_name_option
                        break
                if dicom_folder_name == "":
                    continue

            if os.name == "nt":
                record_date = record_date.split(r"\\")[-1]
            else:
                record_date = record_date.split("/")[-1]
            # check if text is a date and output in isofromat
            record_date_iso = check_if_text_is_a_date_and_output_in_isofromat(record_date)
            if record_date_iso == "":
                continue
            # create a new folder with the iso formatted date as name in the patient folder of the target folder
            if os.name == "nt":
                mkdir_when_not_existent(target_path + r"\\dicom\\" + pseudonym_number + r"\\" + record_date_iso)
            else:
                mkdir_when_not_existent(target_path + "/dicom/" + pseudonym_number + "/" + record_date_iso)
            # check if the recorde date containes a dicom study folder either dicom or Dicom or DICOM, list folder name

            # copy the dicom folder to the new folder
            # check the os system and copy the dicom folder to the new folder
            if os.name == "nt":
                os.system(
                    r"xcopy   " + origin_path + r"\\" + patient_folder + r"\\" + record_date + r"\\" + dicom_folder_name + "  " + target_path + r"\\dicom\\" + pseudonym_number + r"\\" + record_date_iso + r"\\dicom\  /e /y")
                if verbose:
                    print(
                         r"xcopy   " + origin_path + r"\\" + patient_folder + r"\\" + record_date + r"\\" + dicom_folder_name + "  " + target_path + r"\\dicom\\" + pseudonym_number + r"\\" + record_date_iso + r"\\dicom\  /e /y")
            else:
                os.system(
                    f"cp -r {origin_path}/{patient_folder}/{record_date}/{dicom_folder_name}/ {target_path}/dicom/{pseudonym_number}/{record_date_iso}/dicom")
                if verbose:
                    print(
                        f"cp -r {origin_path}/{patient_folder}/{record_date}/{dicom_folder_name}/ {target_path}/dicom/{pseudonym_number}/{record_date_iso}/dicom")
            number_dicoms += 1

    list_niftis = ["T2ax.nii", "t1_3d.nii", "flair_ax.nii"]
    niffis_count = {"T2ax.nii": 0, "t1_3d.nii": 0, "flair_ax.nii": 0}
    for patient_folder_and_pseudonym in patient_folders_and_pseudonyms:

        patient_folder = patient_folder_and_pseudonym[0]
        pseudonym_number = patient_folder_and_pseudonym[1]
        if os.name == "nt":
            record_dates = get_list_of_folders(origin_path + r"\\" + patient_folder)
        else:
            record_dates = get_list_of_folders(origin_path + "/" + patient_folder)
        for record_date in record_dates:
            for nifti in list_niftis:
                # check if the recorde date contains a nifti
                if os.name == "nt":
                    # check if nifti is in the folder or in a subfolder
                    nifti_path = get_path_of_a_file_in_a_folder(origin_path + r"\\" + patient_folder + r"\\" + record_date, nifti)
                    if nifti_path is None:
                        continue
                else:
                    # check if nifti is in the folder or recursively in subfolders
                    nifti_path = get_path_of_a_file_in_a_folder(origin_path + "/" + patient_folder + "/" + record_date, nifti)
                    if nifti_path is None:
                        continue
                if os.name == "nt":
                    record_date = record_date.split(r"\\")[-1]
                else:
                    record_date = record_date.split("/")[-1]
                record_date_iso = check_if_text_is_a_date_and_output_in_isofromat(record_date)
                if record_date_iso == "":
                    continue
                # create a new folder with the iso formatted date as name in the patient folder of the target folder
                if os.name == "nt":
                    mkdir_when_not_existent(target_path + r"\nifti\\" + pseudonym_number + r"\\" + record_date_iso)
                else:
                    mkdir_when_not_existent(target_path + "/nifti/" + pseudonym_number + "/" + record_date_iso)

                # check the os system and copy the dicom folder to the new folder
                if os.name == "nt":
                    os.system(
                        r"xcopy " + nifti_path + r" " + target_path + r"\\nifti\\" + pseudonym_number + r"\\" + record_date_iso + r"\\" + nifti + r"*  /y")
                    if verbose:
                        print(
                            r"xcopy " + nifti_path + r" " + target_path + r"\\nifti\\" + pseudonym_number + r"\\" + record_date_iso + r"\\" + nifti + r"*  /y")
                else:
                    os.system(
                        f"cp {nifti_path} {target_path}/nifti/{pseudonym_number}/{record_date_iso}")
                    if verbose:
                        print(
                            f"cp {nifti_path} {target_path}/nifti/{pseudonym_number}/{record_date_iso}")
                niffis_count[nifti] += 1
    print(f"{number_dicoms} dicoms copied")
    print(f"{niffis_count} nifti copied")
    # for nifti and dicom remove the patient folders without dicom or niftis
    if pseudonymisation:
        # create a csv  from patient_folders_and_pseudonyms list
        with open(target_path + "/patient_folders_and_pseudonyms.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(["patient_folder", "pseudonym_number"])
            for patient_folder_and_pseudonym in patient_folders_and_pseudonyms:
                csv_writer.writerow(patient_folder_and_pseudonym)


if __name__ == '__main__':
    main()