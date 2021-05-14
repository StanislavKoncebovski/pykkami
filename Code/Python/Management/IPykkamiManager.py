from datetime import datetime
import pydicom as dicom
from DicomStuff.DicomMetadata import DicomMetadata
from Taxons.Series import Series
from Taxons.Study import Study
from enumerations import Gender


class IPykkamiManager:
    """
    Interface for pykkami-based applications.
    """

    # region Series Creation
    def create_refurbished_series(self, study: Study, source_file_names: list[str], metadata: DicomMetadata = None) -> Series:
        """
        Creates a "refurbished" series from a number of DICOM files and an instance of DicomMetadata.
        No entries to a database or file system are made. The 'study' value is not assigned.
        :param source_file_names: List of file names to create a series from.
        :param metadata: Dicom metadata to use. If set to None, the default values will be taken.
        :return: An instance of the Series class.
        """

        if not study.is_valid():
            return None

        series = Series()
        study.add_series(series)

        if metadata is None:
            metadata = DicomMetadata()

        series.series_number = metadata.series_number
        series.series_datetime = datetime.now()
        series.series_description = metadata.series_description
        series.modality = metadata.modality
        series.pixel_spacing = metadata.pixel_spacing
        series.image_orientation_patient = metadata.image_orientation_patient
        series.spacing_between_slices = metadata.spacing_between_slices
        series.protocol_name = metadata.protocol_name
        series.sequence_name = metadata.sequence_name
        series.transfer_syntax = metadata.transfer_syntax
        series.sop_class = metadata.sop_class_uid
        series.specific_character_set = metadata.specific_character_set

        for file_name in source_file_names:
            dataset = dicom.read_file(file_name)
            self.assign_series_data(dataset)

    # endregion

    def assign_series_data(self, series: Series, dataset: dicom.dataset):
        """
        Assigns series data to the dataset attributes
        :param series: series to take data from.
        :param dataset: dataset to assign to
        :return:
        """
        dataset.PatientID = series.study.patient.patient_id
        dataset.PatientName = series.study.patient.name
        dataset.PatientBirthDate = series.study.patient.date_of_birth
        dataset.PatientSex = "F" if series.study.patient.gender == Gender.Female else "M" # refine later
        dataset.StudyInstanceUID = series.study.study_uid
        dataset.StudyID = series.study.study_id
        dataset.StudyDescription = series.study.study_description
        dataset.StudyDate = series.study.study_date_time.date
        dataset.StudyTime = series.study.study_date_time.time
        dataset.ReferringPhysicianName = series.study.referring_physician_name
        # ... TODO: to be continued from here ...
