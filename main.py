from utils import get_list_of_folders
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
    origin_path = "/home/davidhieber/Documents/Leucoexpert/test_folder_mris/orgin"
    target_path = "/home/davidhieber/Documents/Leucoexpert/test_folder_mris/target"
    # create the dicom and nifti folder in the target folder if they do not exist
    if not os.path.exists(target_path + "/dicom"):
        os.mkdir(target_path + "/dicom")
    if not os.path.exists(target_path + "/nifti"):
        os.mkdir(target_path + "/nifti")

    patient_folders = get_list_of_folders(origin_path)
    # create the same folders in the target folder if they do not exist
    for patient_folder in patient_folders:
        if not os.path.exists(target_path + "/dicom/" + patient_folder):
            os.mkdir(target_path + "/dicom/" + patient_folder)
        if not os.path.exists(target_path + "/nifti/" + patient_folder):
            os.mkdir(target_path + "/nifti/" + patient_folder)

    number_dicoms = 0
    number_nifti = 0
    # for every patient folder in the origin folder get the list of sub folder names, create a list of iso formatted dates
    for patient_folder in patient_folders:
        record_dates = get_list_of_folders(origin_path + "/" + patient_folder)
        for record_date in record_dates:
            record_date = record_date.split("/")[-1]
            #remove all characters that are not numbers  from te sub folder name
            record_date_iso = record_date.replace(" ", "")
            record_date_iso = record_date_iso.replace("-", "")
            record_date_iso = record_date_iso.replace(":", "")
            record_date_iso = record_date_iso.replace(".", "")
            #check if record_date is a valid date
            if not record_date_iso.isnumeric():
                print(f"not a valid date  {patient_folder}/{record_date}")
                continue
            # check if the recorde date is a valid date
            if not (1900 < int(record_date_iso[:4]) < 2100 and 1 <= int(record_date_iso[4:6]) <= 12 and 1 <= int(record_date_iso[6:8]) <= 31):
                print(f"not a valid date {patient_folder}/{record_date}")
                continue
            # convert to iso formatted date
            record_date_iso = record_date[:4] + "-" + record_date[4:6] + "-" + record_date[6:8]


            # create a new folder with the iso formatted date as name in the patient folder of the target folder
            if not os.path.exists(target_path + "/dicom/" + patient_folder + "/" + record_date_iso):
                os.mkdir(target_path + "/dicom/" + patient_folder + "/" + record_date_iso)
            # check if the recorde date containes a dicom study

            if os.path.exists(origin_path + "/" + patient_folder + "/" + record_date + "/dicom"):
                # copy the dicom folder to the new folder
               # check the os system and copy the dicom folder to the new folder
                if os.name == "nt":
                    os.system(f"copy {origin_path}/{patient_folder}/{record_date}/dicom {target_path}/dicom/{patient_folder}/{record_date_iso}  /E/H")
                else:
                    os.system(f"cp -r {origin_path}/{patient_folder}/{record_date}/dicom {target_path}/dicom/{patient_folder}/{record_date_iso}")
                number_dicoms += 1
    print(f"{number_dicoms} dicoms copied")
    print(f"{number_nifti} nifti copied")


if __name__ == '__main__':
    main()