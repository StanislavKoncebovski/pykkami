from Data.IDicomDatabase import IDicomDatabase
import sqlite3
from sqlite3 import Error
from datetime import date
from Taxons import Patient, Study, Series, Instance


class BasicDicomDatabase(IDicomDatabase):
    # region Protected Data
    _table_patient = "patient"
    _table_study = "study"
    _table_series = "series"
    _table_instance = "instance"

    _sql_create_table_patient = \
        """
        CREATE TABLE IF NOT EXISTS `patient` ( 
        `patient_id`                            VARCHAR(64),
        `patient_name`                          VARCHAR(128),
        `patient_date_of_birth`                 TIME,
        `patient_gender`                        VARCHAR(16),
        PRIMARY KEY(patient_id)
        );
        """

    _sql_create_table_study = \
        """
        CREATE TABLE IF NOT EXISTS `study` (
        `study_uid`						        VARCHAR(64),
        `patient_id`					        VARCHAR(64),
        `study_datetime`				        TIME,
        `referring_physician_name`		        VARCHAR(128),
        `institution_name`                      VARCHAR(128),
        `accession_number`				        VARCHAR(32),
        `study_id`						        VARCHAR(64),
        `study_description`				        TEXT,
        `anatomic_region`                       VARCHAR(16),
        PRIMARY KEY(study_uid)
        );
        """

    _sql_create_table_series = \
        """
        CREATE TABLE IF NOT EXISTS `series` (
        `series_uid`					        VARCHAR(64),
        `study_uid`						        VARCHAR(64),
        `sop_class_uid`                         VARCHAR(64),
        `transfer_syntax`                       VARCHAR(64),
        `specific_character_set`                VARCHAR(128),
        `series_datetime`				        TIME,
        `modality`						        VARCHAR(16),
        `series_number`					        INTEGER,
        `series_description`			        VARCHAR(128),
        `sequence_name`                         VARCHAR(64),
        `protocol_name`                         VARCHAR(64),
        `spacing_between_slices`                FLOAT,
        `pixel_spacing_x`                       FLOAT,
        `pixel_spacing_y`                       FLOAT,
        `image_orientation_patient_rows_x`      FLOAT,
        `image_orientation_patient_rows_y`      FLOAT,
        `image_orientation_patient_rows_z`      FLOAT,
        `image_orientation_patient_columns_x`   FLOAT,
        `image_orientation_patient_columns_y`   FLOAT,
        `image_orientation_patient_columns_z`   FLOAT,
        PRIMARY KEY(series_uid)
        );
        """

    _sql_create_table_instance = \
        """
        CREATE TABLE IF NOT EXISTS `instance` (
        `instance_uid`					VARCHAR(64),
        `series_uid`					VARCHAR(64),
        `instance_number`				INTEGER,
        `image_position_patient_x`      FLOAT,
        `image_position_patient_y`      FLOAT,
        `image_position_patient_z`      FLOAT,
        `file_name`						VARCHAR(256),
        PRIMARY KEY(instance_uid)
        );
        """
    # endregion

    # region  Construction
    def __init__(self):
        self._connection = None
    # endregion

    # region General Management
    def open(self, database_file_name: str):
        """
        Opens the database
        :param database_file_name: The path to the database file
        :return None:
        """
        try:
            self._connection = sqlite3.connect(database_file_name)
            result = self.create_tables()

            if not result:
                raise UserWarning("Tables could not be created")
        except Error as e:
            raise e

    def close(self):
        """
        Closes the database.
        TODO: implement me!
        :return: None
        """
        self.drop_tables()
    # endregion

    # region Patient Management
    def insert_patient(self, patient: Patient):
        """
        Tries to insert a patient.
        :param patient: The patient to insert.
        :return: None.
        :exception: KeyError, if the PatientID is already present in the DB.
        """
        sql = f"INSERT INTO " \
              f"{self._table_patient} " \
              f"VALUES (" \
              f"'{patient.patient_id}', " \
              f"'{patient.name}', " \
              f"'{patient.date_of_birth}', " \
              f"'{patient.gender}'" \
              ")"

        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
        except Error as e:
            raise e

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
        sql = f"SELECT * FROM {self._table_patient} WHERE `patient_id` = '{patient_id}'"
        try:
            # assure return data as dictionary:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchone()

            return self._get_patient(fetched)
        except Error as e:
            return None

    def select_patients_by_name_pattern(self, name_pattern: str) -> list[Patient]:
        """
        Selects a set of patients by name pattern.
        :param name_pattern: The name pattern to select by.
        :return: A list of patients with the names fulfilling the pattern. An empty list if none were found.
        """
        sql = f"SELECT * FROM {self._table_patient} WHERE `patient_name` LIKE '%{name_pattern}%'"

        try:
            # assure return data as dictionary:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchall()

            result = []

            for fetch in fetched:
                patient = self._get_patient(fetch)

                if patient is not None:
                    result.append(patient)

            return result
        except ValueError:
            return []

    def select_patients_by_date_of_birth(self, dob_from: date, dob_to: date) -> list[Patient]:
        """
        Selects a set of patients by date of birth.
        :param dob_from:  The starting date (inclusive).
        :param dob_to: The finishing date (inclusive).
        :return: A list of patients with the dates of birth within the interval.
        """
        sql = f"SELECT * FROM {self._table_patient} WHERE `patient_date_of_birth` >= '{dob_from}' AND `patient_date_of_birth` <= '{dob_to}'"

        try:
            # assure return data as dictionary:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchall()

            result = []

            for fetch in fetched:
                patient = self._get_patient(fetch)

                if patient is not None:
                    result.append(patient)

            return result
        except ValueError:
            return []

    def select_all_patients(self) -> list[Patient]:
        """
        Selects all patients.
        :return: The list of all patients.
        """
        sql = f"SELECT * FROM {self._table_patient}"

        try:
            # assure return data as dictionary:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchall()

            result = []

            for fetch in fetched:
                patient = self._get_patient(fetch)

                if patient is not None:
                    result.append(patient)

            return result
        except ValueError:
            return []

    def select_patients_by_limit(self, limit: int) -> list[Patient]:
        """
        Selects a limited number of patients.
        :param limit: The number of patients to select.
        :return: The list of all patients selected.
        """
        sql = f"SELECT * FROM {self._table_patient} LIMIT {limit}"

        try:
            # assure return data as dictionary:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchall()

            result = []

            for fetch in fetched:
                patient = self._get_patient(fetch)

                if patient is not None:
                    result.append(patient)

            return result
        except ValueError:
            return []
    # endregion

    # region Protected Auxiliary
    def create_tables(self) -> bool:
        result = True
        result &= self._create_table(self._sql_create_table_patient)
        result &= self._create_table(self._sql_create_table_study)
        result &= self._create_table(self._sql_create_table_series)
        result &= self._create_table(self._sql_create_table_instance)

        return result

    def drop_tables(self):
        result = True
        result &= self._drop_table(self._table_patient)
        result &= self._drop_table(self._table_study)
        result &= self._drop_table(self._table_series)
        result &= self._drop_table(self._table_instance)

        return result

    def _create_table(self, sql_creation: str) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql_creation)
            return True
        except Error:
            return False

    def _drop_table(self, table_name: str) -> bool:
        sql = f"DROP TABLE {table_name}"
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            return True
        except Error:
            return False

    def _get_patient(self, fetched: dict) -> Patient:
        try:
            patient = Patient.Patient()
            patient.patient_id = fetched["patient_id"]
            patient.name = fetched["patient_name"]
            patient.date_of_birth = fetched["patient_date_of_birth"]
            patient.gender = fetched["patient_gender"]

            return patient
        except Error as e:
            return None
    # endregion

