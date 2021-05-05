import os.path
import pydicom as dicom
from Data.IDicomStorage import IDicomStorage
from Taxons import Series


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
        pass

    def get_dataset(self, file_path: str) -> dicom.dataset:
        """
        Tries to retrieve a dataset from the file system.
        :param file_path: The full path to the file.
        :return: The dataset, if successful, otherwise None.
        """
        pass

    def append_images(self, series: Series) -> list[str]:
        """
        Retrieves images for a series and appends them to the instances of the series.
        :param series: The series to append images to.
        :return: List of Instance UID's for which images could not be appended.
                 If this list was empty, the operation completely succeeded.
        """
        pass
