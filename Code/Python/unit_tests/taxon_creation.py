import random
from datetime import timedelta, datetime, date
from Taxons.Patient import Patient
from Taxons.Study import Study
from Taxons.Series import Series
from enumerations import Gender, AnatomicRegion, Modality
from faker import Faker


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


def create_patient() -> Patient:
    patient = Patient()

    patient.date_of_birth = create_date_of_birth()

    r = random.randint(0, 100)
    if r <= 50:
        patient.gender = Gender.Female
    else:
        patient.gender = Gender.Male

    patient.name = create_dicom_name_(patient.gender)
    return patient


def create_study() -> Study:
    fake = Faker()

    study = Study()
    study.study_id = f"S_{random.randint(100, 1000)}"
    study.study_description = fake.text(42)
    study.study_date_time = datetime.now()
    study.accession_number = f"AC_{random.randint(100, 1000)}"
    study.anatomic_region = random.choice(list(AnatomicRegion))
    study.institution_name = fake.company()
    study.referring_physician_name = create_dicom_name_()

    return study


def create_series() -> Series:
    fake = Faker()

    series = Series()
    series.series_datetime  = datetime.now()
    series.series_number = random.randint(1, 100)
    series.series_description = fake.text(42)
    series.modality = random.choice(list(Modality))
    series.pixel_spacing = (random.randint(50, 100) / 100, random.randint(50, 100) / 100)
    series.protocol_name = fake.text(42)
    series.sequence_name = fake.text(42)
    series.spacing_between_slices = random.randint(100, 500) / 100

    return series