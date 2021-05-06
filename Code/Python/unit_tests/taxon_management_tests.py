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
