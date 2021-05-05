from Data.IDicomDatabase import IDicomDatabase


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
        `institution:name`                      VARCHAR(128),
        `accession_number`				        VARCHAR(32),
        `study_id`						        VARCHAR(64),
        `study_description`				        TEXT,
        `anatomic_region`                       VARCHAR(16)
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

