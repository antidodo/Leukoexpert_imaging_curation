import sys

from utils import get_list_of_folders, mkdir_when_not_existent, make_list_of_dirs_in_path, \
    check_if_text_is_a_date_and_output_in_isofromat
import  os


def main():
    """
    kuriert ->  dicom(ids(ios_datum(DICOM)))  , Niff(ids(iso_daum(Alle relvanten niffty))

    Main function for the data curation skript.
    At a spesifite path it creates tow sub folders Dicom and nif
    in both folders it creates the same folder with  names from an origin folder
    Then for every created folder it locks in the origin if ther a sub folders with dates as names
    it this is the case it copies the sub folder to the new renamed with iso formateded date as file name
    if ther is a dicom folder in the date folder from the orign folder it copies the dicom folder to the new folder
    same proces is repeated fo the niff folder, but only select secenses get copied
    :return:
    """
    #get the path from the args
    origin_path = sys.argv[1]
    target_path = sys.argv[2]
    if sys.argv[3] == "V":
        verbose = True
    else:
        verbose = False

    if os.name == "nt":
        # create the target path if they do not exist
        mkdir_when_not_existent(target_path)
        # create the dicom and nifti folder in the target folder if they do not exist
        mkdir_when_not_existent(target_path + r"\\dicom")
        mkdir_when_not_existent(target_path + r"\\nifti")
        patient_folders = get_list_of_folders(origin_path)
        # create the same folders in the target folder if they do not exist
        make_list_of_dirs_in_path(target_path + r"\\dicom\\", patient_folders)
        make_list_of_dirs_in_path(target_path + r"\\nifti\\", patient_folders)
        if verbose:
            print(f"patient folders created {patient_folders}")

    else:
        # create the target path if they do not exist
        mkdir_when_not_existent(target_path)
        # create the dicom and nifti folder in the target folder if they do not exist
        mkdir_when_not_existent(target_path + "/dicom")
        mkdir_when_not_existent(target_path + "/nifti")
        patient_folders = get_list_of_folders(origin_path)
        # create the same folders in the target folder if they do not exist
        make_list_of_dirs_in_path(target_path + "/dicom/", patient_folders)
        make_list_of_dirs_in_path(target_path + "/nifti/", patient_folders)
        if verbose:
            print(f"patient folders created {patient_folders}")

    number_dicoms = 0
    # for every patient folder in the origin folder get the list of sub folder names, create a list of iso formatted dates
    for patient_folder in patient_folders:
        if os.name == "nt":
            record_dates = get_list_of_folders(origin_path + r"\\" + patient_folder)
        else:
            record_dates = get_list_of_folders(origin_path + "/" + patient_folder)
        for record_date in record_dates:
            # check if the recorde date containes a dicom study
            dicom_folder_name = ""
            if os.name == "nt":
                if os.path.exists(origin_path + r"\\" + patient_folder + r"\\" + record_date + "/dicom"):
                    dicom_folder_name = "dicom"
                if os.path.exists(origin_path + r"\\"+ patient_folder + r"\\" + record_date + "/Dicom"):
                    dicom_folder_name = "Dicom"
                if os.path.exists(origin_path + r"\\" + patient_folder + r"\\" + record_date + "/DICOM"):
                    dicom_folder_name = "DICOM"
                if dicom_folder_name == "":
                    continue
            else:
                if os.path.exists(origin_path + "/" + patient_folder + "/" + record_date + "/dicom"):
                    dicom_folder_name = "dicom"
                if os.path.exists(origin_path + "/" + patient_folder + "/" + record_date + "/Dicom"):
                    dicom_folder_name = "Dicom"
                if os.path.exists(origin_path + "/" + patient_folder + "/" + record_date + "/DICOM"):
                    dicom_folder_name = "DICOM"
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
                mkdir_when_not_existent(target_path + r"\\dicom\\" + patient_folder + r"\\" + record_date_iso)
            else:
                mkdir_when_not_existent(target_path + "/dicom/" + patient_folder + "/" + record_date_iso)
            # check if the recorde date containes a dicom study folder either dicom or Dicom or DICOM, list folder name

            # copy the dicom folder to the new folder
            # check the os system and copy the dicom folder to the new folder
            if os.name == "nt":
                os.system(r"Copy-Item " + origin_path + r"\\" + patient_folder+ r"\\" + record_date+r"\\"+ dicom_folder_name +" " +target_path+ r"\\dicom\\" + patient_folder+ r"\\" +record_date_iso+ r"\\dicom")
                if verbose:
                    print(r"Copy-Item " + origin_path + r"\\" + patient_folder+ r"\\" + record_date+r"\\"+ dicom_folder_name +" " +target_path+ r"\\dicom\\" + patient_folder+ r"\\" +record_date_iso+ r"\\dicom")
            else:
                os.system(f"cp -r {origin_path}/{patient_folder}/{record_date}/{dicom_folder_name}/ {target_path}/dicom/{patient_folder}/{record_date_iso}/dicom")
                if verbose:
                    print(f"cp -r {origin_path}/{patient_folder}/{record_date}/{dicom_folder_name}/ {target_path}/dicom/{patient_folder}/{record_date_iso}/dicom")
            number_dicoms += 1

    list_niftis = ["T2ax.nii", "t1_3d.nii", "flair_ax.nii"]
    niffis_count = { "T2ax.nii":0, "t1_3d.nii":0, "flair_ax.nii":0}
    for patient_folder in patient_folders:
        if os.name == "nt":
            record_dates = get_list_of_folders(origin_path + r"\\" + patient_folder)
        else:
            record_dates = get_list_of_folders(origin_path + "/" + patient_folder)
        for record_date in record_dates:
            for nifti in list_niftis:
                # check if the recorde date containes a nifti
                if os.name == "nt":
                    if not os.path.exists(origin_path + r"\\" + patient_folder + r"\\" + record_date + r"\\" + nifti):
                        continue
                else:
                    if not os.path.exists(origin_path + "/" + patient_folder + "/" + record_date + "/" + nifti):
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
                    mkdir_when_not_existent(target_path + r"\nifti\\" + patient_folder + r"\\" + record_date_iso)
                else:
                    mkdir_when_not_existent(target_path + "/nifti/" + patient_folder + "/" + record_date_iso)

               # check the os system and copy the dicom folder to the new folder
                if os.name == "nt":
                    os.system(r"copy " + origin_path + r"\\" + patient_folder + r"\\" + record_date + r"\\" + nifti + r" " + target_path + r"\\nifti\\" + patient_folder + r"\\" + record_date_iso + r"\\"+ nifti)
                else:
                    os.system(f"cp {origin_path}/{patient_folder}/{record_date}/{nifti} {target_path}/nifti/{patient_folder}/{record_date_iso}")
                niffis_count[nifti] += 1
    print(f"{number_dicoms} dicoms copied")
    print(f"{niffis_count} nifti copied")
    # for nifti and dicom remove the patient folders without dicom or niftis

if __name__ == '__main__':
    main()