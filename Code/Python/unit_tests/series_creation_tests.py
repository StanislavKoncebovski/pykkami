import os
import unittest

import pydicom.misc

import taxon_creation as cre
from Management.PykkamiManager import PykkamiManager

class SeriesCreationTests(unittest.TestCase):
    def test_creation_of_refurbished_series_succeeds(self):
        patient = cre.create_patient()
        study = cre.create_study()
        patient.add_study(study)
        source_file_names = []

        test_data_folder = "TestData"
        for file_name in os.listdir(test_data_folder):
            abs_file_name = os.path.join(os.getcwd(), test_data_folder, file_name)
            if pydicom.misc.is_dicom(abs_file_name):
                source_file_names.append(abs_file_name)

        series = PykkamiManager.create_refurbished_series(study, source_file_names)

        self.assertIsNotNone(series)
        self.assertEqual(10, len(series.instances))

if __name__ == '__main__':
    unittest.main()


