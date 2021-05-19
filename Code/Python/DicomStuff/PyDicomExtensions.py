import pydicom


def is_dicom(file_name: str) -> bool:
    """
    Checks if a file contains a DICOM object (image or SR, or otherwise).
    A DICOM file has an "DICM" entry after an offset of 0x80 = 128 bytes_read (new standard).
    Older files will not be recognized by this method and stamped as "non-DICOM".
    TODO: alreday implemented in pyDicom!
    :param file_name: The name of the file.
    :return: True, if the file is recognized as DICOM.
    """
    with open(file_name, "rb") as file:
        bytes_read = file.read(132)

        try:
            string = bytes_read[-4:].decode("ascii")
            return string == "DICM"
        except ValueError:
            return False


def is_dicom_image(dataset: pydicom.dataset) -> bool:
    """
    Checks if a dataset is a DICOM image.
    :param dataset: The dataset to check.
    :return: True, if the dataset contains pixel data.
    """
    try:
        element = dataset.data_element("PixelData")
        return element is not None
    except ValueError:
        return False


def is_dicom_image_file(file_name: str) -> bool:
    """
    Checks if a file contains a DICOM image.
    :param file_name: The name of the file.
    :return: True, if the file contains a DICOM object with pixel data.
    """
    try:
        dataset = pydicom.read_file(file_name)
        return is_dicom_image(dataset)
    except ValueError:
        return False


def is_dataset_valid(dataset: pydicom.dataset) -> bool:
    """
    Checks if a dataset is valid. A valid dataset must contain a valid PatientID,
    a valid StudyUID, SeriesUID, and InstanceUID.
    :param dataset: The dataset to check.
    :return: True, if the validation concept holds for the dataset.
    """
    try:
        patient_id = dataset.data_element("PatientID")
        study_uid = dataset.data_element("StudyInstanceUID")
        series_uid = dataset.data_element("SeriesInstanceUID")
        instance_uid = dataset.data_element("SOPInstanceUID")

        if (patient_id is None) or (study_uid is None) or (series_uid is None) or (instance_uid is None):
            return False

        return len(str(patient_id)) > 0 and \
               len(str(study_uid)) > 0 and \
               len(str(series_uid)) > 0 and \
               len(str(instance_uid)) > 0

    except ValueError:
        return False
