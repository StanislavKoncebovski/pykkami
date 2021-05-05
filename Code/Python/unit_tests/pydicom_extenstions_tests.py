import unittest
import pydicom
from DicomStuff import PyDicomExtensions as PDX


class PyDicomExtensionsTests(unittest.TestCase):
    def test_dicom_file_recognition_DICOM_FILE_succeeds(self):
        file_name = "TestData/Image_0001.dcm"
        check = PDX.is_dicom(file_name)

        self.assertTrue(check)

    def test_dicom_file_recognition_NON_DICOM_FILE_succeeds(self):
        file_name = "TestData/ZIP-0004-0001.dcm"
        check = PDX.is_dicom(file_name)

        self.assertFalse(check)

    def test_dicom_image_recognition_DICOM_IMAGE_succeeds(self):
        file_name = "TestData/Image_0001.dcm"
        dataset = pydicom.read_file(file_name)
        check = PDX.is_dicom_image(dataset)

        self.assertTrue(check)

    def test_dicom_dataset_validation_DATASET_VALID_succeeds(self):
        file_name = "TestData/Image_0001.dcm"
        dataset = pydicom.read_file(file_name)
        check = PDX.is_dataset_valid(dataset)

        self.assertTrue(check)