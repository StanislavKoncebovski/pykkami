from datetime import date
from Taxons.Patient import Patient, Study
from Taxons.Series import Series, Instance

class IDicomDatabase:
    """
    Interface of a DICOM-oriented database.
    """
    # region General Management
    def open(self, database_file_name: str):
        """
        Opens the database
        :param database_file_name: The path to the database file
        :return None:
        """
        pass

    def close(self):
        """
        Closes the database.
        :return: None
        """
        pass
    # endregion

    # region Patient Management
    def insert_patient(self, patient: Patient):
        """
        Tries to insert a patient.
        :param patient: The patient to insert.
        :return: None.
        :exception: KeyError, if the PatientID is already present in the DB.
        """
        pass

    def update_patient(self, patient: Patient):
        """
        Tries to update a patient.
        :param patient: An instance of the Patient class with the PatientID of the patient to update (and some new data).
        :return: None.
        :exception: KeyError, if the PatientID was not present.
        """
        pass

    def delete_patient(self, patient_id: str):
        """
        Tries to delete a patient.
        :param patient_id: The PatientID of the patient to delete.
        :return: None.
        :exception: KeyError, if the PatientID was not present.
        """
        pass

    def select_patient(self, patient_id: str) -> Patient:
        """
        Selects a patient by PatientID.
        :param patient_id: The PatientID of the patient to select.
        :return: The patient, if found, otherwise None
        """
        pass

    def select_patients_by_name_pattern(self, name_pattern: str) -> list[Patient]:
        """
        Selects a set of patients by name pattern.
        :param name_pattern: The name pattern to select by.
        :return: A list of patients with the names fulfilling the pattern. An empty list if none were found.
        """
        pass

    def select_patients_by_date_of_birth(self, dob_from: date, dob_to: date) -> list[Patient]:
        """
        Selects a set of patients by date of birth.
        :param dob_from:  The starting date (inclusive).
        :param dob_to: The finishing date (inclusive).
        :return: A list of patients with the dates of birth within the interval.
        """
        pass

    def select_all_patients(self) -> list[Patient]:
        """
        Selects all patients.
        :return: The list of all patients.
        """
        pass

    def select_patients_by_limit(self, limit: int) -> list[Patient]:
        """
        Selects a limited number of patients.
        :param limit: The number of patients to select.
        :return: The list of all patients selected.
        """
        pass
    # endregion

    # region Study Management
    def insert_study(self, study: Study):
        """
        Tries to insert a study.
        :param study: The study to insert. Must be valid (i.e. have a valid Patient reference).
        :return: None.
        :exception: KeyError if the studyUID was already present or if the patient is not yet in the DB.
        """
        pass

    def update_study(self, study: Study):
        """
        Tries to update a study.
        :param study: An instance of the Study class with the StudyUID of the study to update (and some new data).
        :return: None.
        :exception: KeyError, if the StudyUID was not present.
        """
        pass

    def delete_study(self, study_uid: str):
        """
        Tries to delete a study.
        :param study_uid: Tue UID of the study to delete.
        :return: None.
        :exception: KeyError, if the StudyUID was not present.
        """
        pass

    def select_study(self, study_uid: str) -> Study:
        """
        Selects a study by StudyUID.
        :param study_uid: The StudyUID of the study to select.
        :return: The study, if found, otherwise None
        """
        pass

    def select_studies_to_patient(self, patient_id: str) -> list[Study]:
        """
        Selects the studies of a patient.
        :param patient_id: The PatientID of the patient.
        :return: A list of studies of the patient.
        :exception: KeyError, if the PatientID was not present.
        """
        pass
    # endregion

    # region Series Management
    def insert_series(self, series: Series):
        """
        Tries to insert a series.
        :param series: The series to insert. Must be valid (i.e. have a valid Study reference).
        :return: None.
        :exception: KeyError if the SeriesUID was already present or if the study is not yet in the DB.
        """
        pass

    def update_series(self, series: Series):
        """
        Tries to update a study.
        :param series: An instance of the Series class with the SeriesUID of the series to update (and some new data).
        :return: None.
        :exception: KeyError, if the SeriesUID was not present.
        """
        pass

    def delete_series(self, series_uid: str):
        """
        Tries to delete a series.
        :param series_uid: Tue UID of the series to delete.
        :return: None.
        :exception: KeyError, if the SeriesUID was not present.
        """
        pass

    def select_series(self, series_uid: str) -> Series:
        """
        Selects a series by SeriesUID.
        :param series_uid: The SeriesUID of the series to select.
        :return: The series, if found, otherwise None.
        """
        pass

    def select_series_to_study(self, study_uid: str) -> list[Series]:
        """
        Selects the series of a study.
        :param study_uid: The StudyUID of the study.
        :return: A list of series of the study.
        :exception: KeyError, if the StudyUID was not present.
        """
        pass
    # endregion

    # region Instance Management
    def insert_instance(self, instance: Instance):
        """
        Tries to insert an instance.
        :param instance: The instance to insert. Must be valid (i.e. have a valid Series reference).
        :return: None.
        :exception: KeyError if the InstanceUID was already present or if the series is not yet in the DB.
        """
        pass

    def update_instance(self, instance: Instance):
        """
        Tries to update an instance.
        :param instance: An instance of the Instance class with the InstanceUID of the instance to update (and some new data).
        :return: None.
        :exception: KeyError, if the InstanceUID was not present.
        """
        pass

    def delete_instance(self, instance_uid: str):
        """
        Tries to delete an instance.
        :param instance_uid: Tue UID of the instance to delete.
        :return: None.
        :exception: KeyError, if the InstanceUID was not present.
        """
        pass

    def delete_instances_of_series(self, series_uid: str):
        """
        Deletes all instances of a series.
        :param series_uid: The UID of the series whose instances to delete.
        :return: None.
        :exception: KeyError, if the SeriesUID was not present.
        """
        pass

    def select_instance(self, instance_uid: str) -> Instance:
        """
        Selects an instance by InstanceUID.
        :param instance_uid: The InstanceUID of the instance to select.
        :return: The instance, if found, otherwise None.
        """
        pass

    def select_instances_to_series(self, series_uid: str) -> list[Instance]:
        """
        Selects the instances of a series.
        :param series_uid: The SeriesUID of the series.
        :return: A list of instance of the series.
        :exception: KeyError, if the SeriesUID was not present.
        """
        pass
    # endregion
