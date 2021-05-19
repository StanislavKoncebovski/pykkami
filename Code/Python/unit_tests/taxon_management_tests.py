import unittest
from unit_tests.taxon_creation import *


class TaxonManagementTests(unittest.TestCase):
    def test_creation_of_patient_succeeds(self):
        patient = create_patient()
        print(patient)


    def test_creation_of_study_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)
        print(patient)

    def test_creation_of_series_succeeds(self):
        patient = create_patient()
        study = create_study()
        patient.add_study(study)
        series = create_series()

        print(series)
        study.add_series(series)

    def test_creation_of_multiple_patients_with_multiple_studies_succeeds(self):
        number_of_patients = 3
        number_of_studies = 2

        patients = []

        for f in range(number_of_patients):
            patient = Patient()
            patients.append(patient)

            for p in range(number_of_persons):
                person = Person()
                family.add_person(person)

        # patients = [create_patient() for p in range(number_of_patients)]
        #
        # for patient in patients:
        #     for s in range(number_of_studies):
        #         study = create_study()
        #         patient.add_study(study)
        #
        # self.assertEqual(number_of_patients, len(patients))
        # patient = patients[0]

        self.assertEqual(number_of_studies, len(patient._studies))
