import os
import unittest
import shutil
import pydicom as dicom
from Data.BasicDicomStorage import BasicDicomStorage


class DicomStorageTests(unittest.TestCase):

    _root_folder: str = "./DicomFiles"
    _storageManager = BasicDicomStorage()

    def setUp(self) -> None:
        try:
            self._storageManager.initialize(self._root_folder)
        except OSError:
            self.fail("Creation of root folder failed")

    def tearDown(self):
        shutil.rmtree(self._root_folder, ignore_errors=True)

    def test_creation_of_root_folder_succeeds(self):
        try:
            self._storageManager.initialize(self._root_folder)
        except OSError:
            self.fail("Creation of root folder failed")

    def test_storage_of_dataset_succeeds(self):
        file_name = "./TestData/Image_0001.dcm"
        dataset = dicom.read_file(file_name)

        self._storageManager.store_dataset(dataset)
        self.assertTrue(os.path.isfile(file_name))
        # TODO: test that the DB entry for the path has been made

    def test_retrieval_of_dataset_succeeds(self):
        file_name = "./TestData/Image_0001.dcm"
        dataset = dicom.read_file(file_name)
        self._storageManager.store_dataset(dataset)

        patient_id = dataset.data_element("PatientID").value
        study_uid = dataset.data_element("StudyInstanceUID").value
        series_uid = dataset.data_element("SeriesInstanceUID").value
        instance_uid = dataset.data_element("SOPInstanceUID").value

        path = os.path.join(self._root_folder, patient_id, study_uid, series_uid, instance_uid) + ".dcm"
        dataset1 = dicom.read_file(path)

        self.assertIsNotNone(dataset1)

    def test_append_images_to_series(self):
        pass
        # TODO to be added later
