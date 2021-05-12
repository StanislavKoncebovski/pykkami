from Data.IDicomDatabase import IDicomDatabase
import sqlite3
from sqlite3 import Error
from datetime import date, datetime
from Taxons import Patient, Study, Series, Instance
from enumerations import Gender, AnatomicRegion, Modality
import DataTypes


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
        try:
            self.delete_patient(patient.patient_id)
            self.insert_patient(patient)
        except Error as e:
            raise e

    def delete_patient(self, patient_id: str):
        """
        Tries to delete a patient.
        :param patient_id: The PatientID of the patient to delete.
        :return: None.
        :exception: KeyError, if the PatientID was not present.
        """
        sql = f"DELETE FROM {self._table_patient} WHERE `patient_id` = '{patient_id}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()

            if cursor.lastrowid < 0:
                raise ValueError("deletion of patient failed")

        except Error as e:
            raise e

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
        return self._select_patients(sql)


    def select_patients_by_date_of_birth(self, dob_from: date, dob_to: date) -> list[Patient]:
        """
        Selects a set of patients by date of birth.
        :param dob_from:  The starting date (inclusive).
        :param dob_to: The finishing date (inclusive).
        :return: A list of patients with the dates of birth within the interval.
        """
        sql = f"SELECT * FROM {self._table_patient} WHERE `patient_date_of_birth` >= '{dob_from}' AND `patient_date_of_birth` <= '{dob_to}'"
        return self._select_patients(sql)

    def select_all_patients(self) -> list[Patient]:
        """
        Selects all patients.
        :return: The list of all patients.
        """
        sql = f"SELECT * FROM {self._table_patient}"
        return self._select_patients(sql)

    def select_patients_by_limit(self, limit: int) -> list[Patient]:
        """
        Selects a limited number of patients.
        :param limit: The number of patients to select.
        :return: The list of all patients selected.
        """
        sql = f"SELECT * FROM {self._table_patient} LIMIT {limit}"
        return self._select_patients(sql)
    # endregion

    # region Study Management
    def insert_study(self, study: Study):
        """
        Tries to insert a study.
        :param study: The study to insert. Must be valid (i.e. have a valid Patient reference).
        :return: None.
        :exception: KeyError if the studyUID was already present or if the patient is not yet in the DB.
        """
        sql = f"INSERT INTO " \
              f"{self._table_study} " \
              f"VALUES (" \
              f"'{study.study_uid}', " \
              f"'{study.patient.patient_id}', " \
              f"'{study.study_date_time}', " \
              f"'{study.referring_physician_name}'," \
              f"'{study.institution_name}',"\
              f"'{study.accession_number}'," \
              f"'{study.study_id}'," \
              f"'{study.study_description}'," \
              f"'{study.anatomic_region}'" \
              ")"

        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
        except Error as e:
            raise e

    def update_study(self, study: Study):
        """
        Tries to update a study.
        :param study: An instance of the Study class with the StudyUID of the study to update (and some new data).
        :return: None.
        :exception: KeyError, if the StudyUID was not present.
        """
        try:
            self.delete_study(study.study_uid)
            self.insert_study(study)
        except Error as e:
            raise e

    def delete_study(self, study_uid: str):
        """
        Tries to delete a study.
        :param study_uid: Tue UID of the study to delete.
        :return: None.
        :exception: KeyError, if the StudyUID was not present.
        """
        sql = f"DELETE FROM {self._table_study} WHERE `study_uid` = '{study_uid}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()

            if cursor.lastrowid < 0:
                raise ValueError("deletion of study failed")

        except Error as e:
            raise e

    def select_study(self, study_uid: str) -> Study:
        """
        Selects a study by StudyUID.
        :param study_uid: The StudyUID of the study to select.
        :return: The study, if found, otherwise None
        """
        sql = f"SELECT * FROM {self._table_study} WHERE `study_uid` = '{study_uid}'"
        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchone()

            return self._get_study(fetched)
        except Error as e:
            return None

    def select_studies_to_patient(self, patient_id: str) -> list[Study]:
        """
        Selects the studies of a patient.
        :param patient_id: The PatientID of the patient.
        :return: A list of studies of the patient.
        :exception: KeyError, if the PatientID was not present.
        """
        sql = f"SELECT * FROM {self._table_study} WHERE `patient_id` = '{patient_id}'"

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        fetched = cursor.fetchall()

        result = []

        for fetch in fetched:
            study = self._get_study(fetch)

            if study is not None:
                result.append(study)

        return result
    # endregion

    # region Series Management
    def insert_series(self, series: Series):
        """
        Tries to insert a series.
        :param series: The series to insert. Must be valid (i.e. have a valid Study reference).
        :return: None.
        :exception: KeyError if the SeriesUID was already present or if the study is not yet in the DB.
        """
        charsets = str.join('\\', series.specific_character_set)
        sql = f"INSERT INTO {self._table_series} " \
              f"VALUES(" \
              f"'{series.series_uid}', " \
              f"'{series.study.study_uid}', " \
              f"'{series.sop_class}', " \
              f"'{series.transfer_syntax}'," \
              f"'{charsets}', " \
              f"'{series.series_datetime}', " \
              f"'{series.modality}', " \
              f"{series.series_number}, " \
              f"'{series.series_description}', " \
              f"'{series.sequence_name}', " \
              f"'{series.protocol_name}', " \
              f"{series.spacing_between_slices}, " \
              f"{series.pixel_spacing[0]}, " \
              f"{series.pixel_spacing[1]}, " \
              f"{series.image_orientation_patient[0][0]}, " \
              f"{series.image_orientation_patient[0][1]}, " \
              f"{series.image_orientation_patient[0][2]}, " \
              f"{series.image_orientation_patient[1][0]}, " \
              f"{series.image_orientation_patient[1][1]}, " \
              f"{series.image_orientation_patient[1][2]} " \
              f")"

        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
        except Error as e:
            raise e

    def update_series(self, series: Series):
        """
        Tries to update a study.
        :param series: An instance of the Series class with the SeriesUID of the series to update (and some new data).
        :return: None.
        :exception: KeyError, if the SeriesUID was not present.
        """
        try:
            self.delete_series(series.series_uid)
            self.insert_series(series)
        except Error as e:
            raise e

    def delete_series(self, series_uid: str):
        """
        Tries to delete a series.
        :param series_uid: Tue UID of the series to delete.
        :return: None.
        :exception: KeyError, if the SeriesUID was not present.
        """
        sql = f"DELETE FROM {self._table_series} WHERE `series_uid` = '{series_uid}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()

            if cursor.lastrowid < 0:
                raise ValueError("deletion of study failed")

        except Error as e:
            raise e

    def select_series(self, series_uid: str) -> Series:
        """
        Selects a series by SeriesUID.
        :param series_uid: The SeriesUID of the series to select.
        :return: The series, if found, otherwise None.
        """
        sql = f"SELECT * FROM {self._table_series} WHERE `series_uid` = '{series_uid}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchone()

            return self._get_series(fetched)
        except Error as e:
            return None

    def select_series_to_study(self, study_uid: str) -> list[Series]:
        """
        Selects the series of a study.
        :param study_uid: The StudyUID of the study.
        :return: A list of series of the study.
        :exception: KeyError, if the StudyUID was not present.
        """
        sql = f"SELECT * FROM {self._table_series} WHERE `study_uid` = '{study_uid}'"

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        fetched = cursor.fetchall()

        result = []

        for fetch in fetched:
            series = self._get_series(fetch)

            if series is not None:
                result.append(series)

        return result
    # endregion

    # region Instance Management
    def insert_instance(self, instance: Instance):
        """
        Tries to insert an instance.
        :param instance: The instance to insert. Must be valid (i.e. have a valid Series reference).
        :return: None.
        :exception: KeyError if the InstanceUID was already present or if the series is not yet in the DB.
        """
        sql = f"INSERT INTO {self._table_instance} " \
              f"VALUES(" \
              f"'{instance.instance_uid}', " \
              f"'{instance.series.series_uid}', " \
              f"{instance.instance_number}," \
              f"{instance.instance_position_patient.X}," \
              f"{instance.instance_position_patient.Y},"\
              f"{instance.instance_position_patient.Z}," \
              f"'{instance.file_name}'" \
              f")"

        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
        except Error as e:
            raise e

    def update_instance(self, instance: Instance):
        """
        Tries to update an instance.
        :param instance: An instance of the Instance class with the InstanceUID of the instance to update (and some new data).
        :return: None.
        :exception: KeyError, if the InstanceUID was not present.
        """
        try:
            self.delete_instance(instance.instance_uid)
            self.insert_instance(instance)
        except Error as e:
            raise e

    def delete_instance(self, instance_uid: str):
        """
        Tries to delete an instance.
        :param instance_uid: Tue UID of the instance to delete.
        :return: None.
        :exception: KeyError, if the InstanceUID was not present.
        """
        sql = f"DELETE FROM {self._table_instance} WHERE `instance_uid` = '{instance_uid}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()

            if cursor.lastrowid < 0:
                raise ValueError("deletion of study failed")

        except Error as e:
            raise e

    def delete_instances_of_series(self, series_uid: str):
        """
        Deletes all instances of a series.
        :param series_uid: The UID of the series whose instances to delete.
        :return: None.
        :exception: KeyError, if the SeriesUID was not present.
        """
        sql = f"DELETE FROM {self._table_instance} WHERE `series_uid` = '{series_uid}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()

            if cursor.lastrowid < 0:
                raise ValueError("deletion of study failed")

        except Error as e:
            raise e

    def select_instance(self, instance_uid: str) -> Instance:
        """
        Selects an instance by InstanceUID.
        :param instance_uid: The InstanceUID of the instance to select.
        :return: The instance, if found, otherwise None.
        """
        sql = f"SELECT * FROM {self._table_instance} WHERE `instance_uid` = '{instance_uid}'"

        try:
            self._connection.row_factory = sqlite3.Row
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
            fetched = cursor.fetchone()

            return self._get_instance(fetched)
        except Error as e:
            return None

    def select_instances_to_series(self, series_uid: str) -> list[Instance]:
        """
        Selects the instances of a series.
        :param series_uid: The SeriesUID of the series.
        :return: A list of instance of the series.
        :exception: KeyError, if the SeriesUID was not present.
        """
        sql = f"SELECT * FROM {self._table_instance} WHERE `series_uid` = '{series_uid}'"

        self._connection.row_factory = sqlite3.Row
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        fetched = cursor.fetchall()

        result = []

        for fetch in fetched:
            instance = self._get_instance(fetch)

            if instance is not None:
                result.append(instance)

        return result
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
            patient.date_of_birth = date.fromisoformat(fetched["patient_date_of_birth"])
            patient.gender = Gender[fetched["patient_gender"].replace("Gender.", "")]

            return patient
        except Error as e:
            return None

    def _get_study(self, fetched: dict) -> Study:
        if fetched is None:
            return None

        try:
            study = Study.Study()
            study.study_uid = fetched["study_uid"]
            study.study_date_time = datetime.fromisoformat(fetched["study_datetime"])
            study.referring_physician_name = fetched["referring_physician_name"]
            study.institution_name = fetched["institution_name"]
            study.accession_number = fetched["accession_number"]
            study.study_id = fetched["study_id"]
            study.study_description = fetched["study_description"]
            study.anatomic_region = AnatomicRegion[fetched["anatomic_region"].replace("AnatomicRegion.", "")]

            return study
        except Error as e:
            return None

    def _get_series(self, fetched: dict) -> Series:
        if fetched is None:
            return None

        try:
            series = Series.Series()
            series.series_uid = fetched["series_uid"]
            series.sop_class = fetched["sop_class_uid"]
            series.transfer_syntax = fetched["transfer_syntax"]
            charsets = fetched["specific_character_set"]
            series.specific_character_set = charsets.split("\\")
            series.series_datetime = datetime.fromisoformat(fetched["series_datetime"])
            series.modality = Modality[fetched["modality"].replace("Modality.", "")]
            series.series_number = int(fetched["series_number"])
            series.series_description = fetched["series_description"]
            series.sequence_name = fetched["sequence_name"]
            series.protocol_name = fetched["protocol_name"]
            series.spacing_between_slices = float(fetched["spacing_between_slices"])
            x = float(fetched["pixel_spacing_x"])
            y = float(fetched["pixel_spacing_y"])
            series.pixel_spacing = (x, y)

            x = float(fetched["image_orientation_patient_rows_x"])
            y = float(fetched["image_orientation_patient_rows_y"])
            z = float(fetched["image_orientation_patient_rows_z"])

            vp_rows = (x, y, z)

            x = float(fetched["image_orientation_patient_columns_x"])
            y = float(fetched["image_orientation_patient_columns_y"])
            z = float(fetched["image_orientation_patient_columns_z"])

            vp_columns = (x, y, z)

            series.image_orientation_patient = (vp_rows, vp_columns)

            return series
        except Error as e:
            return None

    def _get_instance(self, fetched: dict) -> Instance:
        try:
            instance = Instance.Instance()

            instance.instance_uid = fetched["instance_uid"]
            instance.instance_number = int(fetched["instance_number"])

            x = float(fetched["image_position_patient_x"])
            y = float(fetched["image_position_patient_z"])
            z = float(fetched["image_position_patient_z"])

            instance.instance_position_patient = (x, y, z)

            instance.file_name = fetched["file_name"]

            return instance
        except Error as e:
            return None

    def _select_patients(self, sql: str):
        try:
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

