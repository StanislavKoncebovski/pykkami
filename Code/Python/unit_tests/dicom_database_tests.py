import unittest
from unit_tests.taxon_creation import *
from Data.BasicDicomDatabase import BasicDicomDatabase


class DicomDataBaseTests(unittest.TestCase):
    _database_file_path = ".\pikkami_test.db3"
    _database: BasicDicomDatabase = None

    def setUp(self):
        self._database = BasicDicomDatabase()
        self._database.open(self._database_file_path)

    def tearDown(self):
        self._database.close()

    def test_insertion_of_patient_NEW_PATIENT_succeeds(self):
        patient = create_patient()
        self._database.insert_patient(patient)

        patient1 = self._database.select_patient(patient.patient_id)

        self.assertIsNotNone(patient1)