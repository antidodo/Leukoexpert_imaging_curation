

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
    origin_path = "D:/Leukoregister/data"
    dicom_path = "D:/Leukoregister/curated/dicom"
    niff_path = "D:/Leukoregister/curated/niff"


if __name__ == '__main__':
    main()