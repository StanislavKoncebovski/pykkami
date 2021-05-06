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

    def test_insertion_of_many_patients_NAME_PATTERN_succeeds(self):
        patients = [create_patient() for i in range(6)]

        patients[0].name = "Aardvark^Aaron"
        patients[1].name = "Aardvark^Berta"
        patients[5].name = "Aardberg^Zenobia"

        for patient in patients:
            self._database.insert_patient(patient)

        fetched = self._database.select_patients_by_name_pattern("Aar")

        self.assertEqual(3, len(fetched))

    def test_insertion_of_many_patients_DOB_succeeds(self):
        patients = [create_patient() for i in range(6)]

        patients[0].date_of_birth = date(1930, 12, 10)
        patients[1].date_of_birth = date(1930, 12, 11)
        patients[5].date_of_birth = date(1930, 12, 12)

        for patient in patients:
            self._database.insert_patient(patient)

        dob_from = date(1930, 12, 1)
        dob_to = date(1930, 12, 15)
        fetched = self._database.select_patients_by_date_of_birth(dob_from, dob_to)

        self.assertEqual(3, len(fetched))

    def test_insertion_of_many_patients_ALL_succeeds(self):
        patients = [create_patient() for i in range(16)]

        for patient in patients:
            self._database.insert_patient(patient)

        fetched = self._database.select_all_patients()

        self.assertEqual(16, len(fetched))

        for fetch in fetched:
            print(fetch)

    def test_insertion_of_many_patients_LIMIT_succeeds(self):
        patients = [create_patient() for i in range(16)]

        for patient in patients:
            self._database.insert_patient(patient)

        fetched = self._database.select_patients_by_limit(10)

        self.assertEqual(10, len(fetched))

        for fetch in fetched:
            print(fetch)

    def test_deletion_of_patient_succeeds(self):
        patients = [create_patient() for i in range(10)]

        for patient in patients:
            self._database.insert_patient(patient)

        self._database.delete_patient(patient_id=patients[0].patient_id)

        fetched = self._database.select_all_patients()

        self.assertEqual(9, len(fetched))

    def test_updating_patient_succeeds(self):
        patient = create_patient()
        patient.name = "Aardvark^Aaron"
        patient.date_of_birth = date(1999, 9, 19)
        patient.gender = Gender.Other
        
        self._database.update_patient(patient)
        patient1 = self._database.select_patient(patient.patient_id)

        self.assertEqual(patient.patient_id, patient1.patient_id)
        self.assertEqual(patient1.name, "Aardvark^Aaron")
        self.assertEqual(patient1.date_of_birth, date(1999, 9, 19))
        self.assertEqual(patient1.gender, Gender.Other)
