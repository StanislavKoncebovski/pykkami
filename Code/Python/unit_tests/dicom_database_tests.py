import unittest
from unit_tests.taxon_creation import *
from DicomStuff.DicomUidProvider import DicomUidProvider
from Data.BasicDicomDatabase import BasicDicomDatabase


class DicomDataBaseTests(unittest.TestCase):
    _database_file_path = ".\pikkami_test.db3"
    _database: BasicDicomDatabase = None

    def setUp(self):
        self._database = BasicDicomDatabase()
        self._database.open(self._database_file_path)

    def tearDown(self):
        self._database.close()

    # region Patient Management Tests
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
    # endregion

    # region Study management tests
    def test_insertion_of_study_NEW_STUDY_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        study1 = self._database.select_study(study.study_uid)
        self.assertIsNotNone(study1)

    def test_selection_of_study_STUDY_EXISTS_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        study1 = self._database.select_study(study.study_uid)
        self.assertIsNotNone(study1)

    def test_selection_of_study_INVALID_UID_returns_None(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        study_uid = study.study_uid[:-1]
        study1 = self._database.select_study(study_uid)
        self.assertIsNone(study1)

    def test_selection_of_studies_to_patient_VALID_PATIENT_succeeds(self):
        patient = create_patient()

        number_of_studies = 4
        studies = [patient.add_study(create_study()) for i in range(number_of_studies)]

        for study_uid in patient._studies:
            study = patient._studies[study_uid]
            patient.add_study(study)
            self._database.insert_study(study)

        studies1 = self._database.select_studies_to_patient(patient.patient_id)

        self.assertEqual(number_of_studies, len(studies1))

    def test_selection_of_studies_to_patient_INVALID_PATIENT_returns_empty_list(self):
        patient = create_patient()

        number_of_studies = 4
        studies = [patient.add_study(create_study()) for i in range(number_of_studies)]

        for study_uid in patient._studies:
            study = patient._studies[study_uid]
            patient.add_study(study)
            self._database.insert_study(study)

        patient_id = patient.patient_id[:-1]

        studies1 = self._database.select_studies_to_patient(patient_id)

        self.assertEqual(0, len(studies1))

    def test_deletion_of_study_STUDY_EXISTS_succeeds(self):
        patient = create_patient()

        number_of_studies = 4
        studies = [patient.add_study(create_study()) for i in range(number_of_studies)]

        for study_uid in patient._studies:
            study = patient._studies[study_uid]
            patient.add_study(study)
            self._database.insert_study(study)

        study_uid = list(patient._studies.keys())[1]

        self._database.delete_study(study_uid)

        studies1 = self._database.select_studies_to_patient(patient.patient_id)

        self.assertEqual(number_of_studies - 1, len(studies1))

    def test_deletion_of_study_STUDY_NOT_EXISTS_changes_nothing(self):
        patient = create_patient()

        number_of_studies = 4
        studies = [patient.add_study(create_study()) for i in range(number_of_studies)]

        for study_uid in patient._studies:
            study = patient._studies[study_uid]
            patient.add_study(study)
            self._database.insert_study(study)

        study_uid = DicomUidProvider.create_study_uid()

        self._database.delete_study(study_uid)

        studies1 = self._database.select_studies_to_patient(patient.patient_id)

        self.assertEqual(number_of_studies, len(studies1))

    def test_updating_study_suceeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        physician = study.referring_physician_name

        study.referring_physician_name = create_dicom_name_()

        self._database.update_study(study)

        study1 = self._database.select_study(study.study_uid)

        self.assertNotEqual(physician, study1.referring_physician_name)
    # endregion

    # region Series Management Tests
    def test_insertion_of_series_NEW_SERIES_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)
        series = create_series()
        study.add_series(series)

        self._database.insert_patient(patient)
        self._database.insert_study(study)
        self._database.insert_series(series)

        series1 = self._database.select_series(series.series_uid)

        self.assertIsNotNone(series1)

    def test_selection_of_series_SERIES_EXISTS_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)
        series = create_series()
        study.add_series(series)

        self._database.insert_patient(patient)
        self._database.insert_study(study)
        self._database.insert_series(series)

        series1 = self._database.select_series(series.series_uid)

        self.assertIsNotNone(series1)

    def test_selection_of_series_INVALID_UID_returns_None(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)
        series = create_series()
        study.add_series(series)

        self._database.insert_patient(patient)
        self._database.insert_study(study)
        self._database.insert_series(series)

        series_uid = series.series_uid[:-1]
        series1 = self._database.select_series(series_uid)

        self.assertIsNone(series1)

    def test_selection_of_seriez_to_study_VALID_STUDY_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        number_of_series = 4

        for i in range(number_of_series):
            series = create_series()
            study.add_series(series)
            self._database.insert_series(series)

        seriez = self._database.select_series_to_study(study.study_uid)

        self.assertIsNotNone(seriez)
        self.assertEqual(number_of_series, len(study._seriez))


    def test_selection_of_seriez_to_study_INVALID_STUDY_returns_empty_list(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        number_of_series = 4

        for i in range(number_of_series):
            series = create_series()
            study.add_series(series)
            self._database.insert_series(series)

        study_uid = study.study_uid[:-1]
        seriez = self._database.select_series_to_study(study_uid)

        self.assertIsNotNone(seriez)
        self.assertEqual(0, len(seriez))

    def test_deletion_of_series_SERIES_EXISTS_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        number_of_series = 4

        for i in range(number_of_series):
            series = create_series()
            study.add_series(series)
            self._database.insert_series(series)

        series_uid = list(study._seriez.keys())[0]

        self._database.delete_series(series_uid)

        seriez = self._database.select_series_to_study(study.study_uid)

        self.assertIsNotNone(seriez)
        self.assertEqual(number_of_series - 1, len(seriez))

    def test_deletion_of_series_SERIES_NOT_EXISTS_changes_nothing(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)

        self._database.insert_patient(patient)
        self._database.insert_study(study)

        number_of_series = 4

        for i in range(number_of_series):
            series = create_series()
            study.add_series(series)
            self._database.insert_series(series)

        series_uid = DicomUidProvider.create_series_uid()

        self._database.delete_series(series_uid)

        seriez = self._database.select_series_to_study(study.study_uid)

        self.assertIsNotNone(seriez)
        self.assertEqual(number_of_series, len(seriez))

    def test_updating_series_suceeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)
        series = create_series()
        series.modality = Modality.CT
        study.add_series(series)

        self._database.insert_patient(patient)
        self._database.insert_study(study)
        self._database.insert_series(series)

        old_modality = series.modality

        series.modality = Modality.MR

        self._database.update_series(series)

        series1 = self._database.select_series(series.series_uid)

        self.assertNotEqual(old_modality, series1.modality)

    # endregion
