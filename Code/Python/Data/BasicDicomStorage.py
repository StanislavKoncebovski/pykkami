import os.path
import pydicom as dicom
from Data.IDicomStorage import IDicomStorage
from Taxons import Series
from DicomStuff import PyDicomExtensions as PDX


class BasicDicomStorage(IDicomStorage):
    """
    Interface of the file system DICOM storage.
    The structure of the system is as follows:
    root
      |
      +-Patient_1
           |
           +-Study_1
               |
               +-Series_1
              |    |
              |    +-Image_1
              |    +-Image_2
              |      ...
              |    +-Image_N
              +- Series_2
           +-Study_2
     +-Patient_2
       ...
     +-Patient_N

    """

    def __init__(self):
        self._root_folder = ""

    # region Properties
    @property
    def root_folder(self) -> str:
        """
        Gets the root folder of the storage file system.
        :return: The name of the root folder.
        """
        return self._root_folder

    # endregion

    def initialize(self, root_folder_: str):
        """
        Initializes the root folder of the storage file system.
        :param root_folder_: The name of the root folder to create.
        :return:
        """
        try:
            self._root_folder = root_folder_
            if not os.path.isdir(self._root_folder):
                os.mkdir(self._root_folder)
        except IOError:
            pass

    def store_dataset(self, dataset: dicom.dataset):
        """
        Tries to store a DICOM dataset in the file system. The full path name to the file is
        <root_folder>/<patient_id>/<study_uid>/<series_uid>/<instance_uid>.dcm .
        If the dataset could be stored, makes an entry into the database ('file_name').
        :param dataset: The dataset to store. Must be valid, i.e. contain all the UID's to build the full path name.
        :return: None.
        :exception: IOError if the dataset could not be stored.
        """
        if not PDX.is_dataset_valid(dataset):
            raise IOError("Dataset not valid")

        patient_id = dataset.data_element("PatientID")
        study_uid = dataset.data_element("StudyInstanceUID")
        series_uid = dataset.data_element("SeriesInstanceUID")
        instance_uid = dataset.data_element("SOPInstanceUID")

        patient_folder = os.path.join(self._root_folder, patient_id.value)
        if not os.path.isdir(patient_folder):
            os.mkdir(patient_folder)

        study_folder = os.path.join(patient_folder, study_uid.value)
        if not os.path.isdir(study_folder):
            os.mkdir(study_folder)

        series_folder = os.path.join(study_folder, series_uid.value)
        if not os.path.isdir(series_folder):
            os.mkdir(series_folder)

        file_name = os.path.join(series_folder, instance_uid.value) + ".dcm"

        try:
            dataset.save_as(file_name)
            # TODO: add file name to the database
        except:
            raise IOError(f"Failed to save dataset at {file_name}")

    def get_dataset(self, file_path: str) -> dicom.dataset:
        """
        Tries to retrieve a dataset from the file system.
        :param file_path: The full path to the file.
        :return: The dataset, if successful, otherwise None.
        """
        try:
            dataset = dicom.read_file(file_path)
            return dataset
        except ValueError:
            return None

    def append_images(self, series: Series) -> list[str]:
        """
        Retrieves images for a series and appends them to the instances of the series.
        :param series: The series to append images to.
        :return: List of Instance UID's for which images could not be appended.
                 If this list was empty, the operation completely succeeded.
        """
        series._instances.clear()

        errors = []

        for instance_uid in series._instances.keys():
            file_path = ""  # TODO: get the file path from the database
            dataset = self.get_dataset(file_path)

            if dataset is not None:
                series._instances[instance_uid].dicom_dataset = dataset
            else:
                errors.append(instance_uid)

        return errors

