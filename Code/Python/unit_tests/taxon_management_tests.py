import unittest
from faker import Faker
import random
from datetime import datetime, date, timedelta
from Taxons.Instance import Instance
from Taxons.Patient import Patient
from enumerations import Gender


def create_date_of_birth():
    year = random.randint(1900, 1990)
    dob = date(year, 1, 1)
    days = random.randint(0, 365)
    dob = dob + timedelta(days=days)

    return dob


def create_dicom_name_(gender: Gender = Gender.Unknown):
    fake = Faker()
    family_name = fake.last_name()
    given_name = ""
    if gender == Gender.Female:
        given_name = fake.first_name_female()
    elif gender == Gender.Male:
        given_name = fake.first_name_male()
    else:
        given_name = fake.first_name_nonbinary()

    return f"{family_name}^{given_name}"


class TaxonManagementTests(unittest.TestCase):
    def test_creation_of_patient_succeeds(self):
        patient = Patient()

        patient.date_of_birth = create_date_of_birth()

        r = random.randint(0, 100)
        if r <= 50:
            patient.gender = Gender.Female
        else:
            patient.gender = Gender.Male
        
        patient.name = create_dicom_name_(patient.gender)

        print(patient)

        instance = Instance()
        print(instance)
