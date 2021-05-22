from datetime import datetime
import pydicom as dicom

from DicomStuff.DicomMetadata import DicomMetadata
from Taxons.Patient import Patient
from Taxons.Series import Series
from Taxons.Study import Study
from enumerations import Gender
from DataTypes import *
from DicomStuff.DicomUidProvider import DicomUidProvider


def assign_series_data(series: Series, dataset: dicom.dataset):
    """
    Assigns series data to the dataset attributes
    :param series: series to take data from.
    :param dataset: dataset to assign to
    :return:
    """
    dataset.PatientID = series.study.patient.patient_id
    dataset.PatientName = series.study.patient.name
    dataset.PatientBirthDate = series.study.patient.date_of_birth
    # TODO: the assignment below is awkward, replace it with a function
    dataset.PatientSex = "F" if series.study.patient.gender == Gender.Female else "M"

    dataset.StudyInstanceUID = series.study.study_uid
    dataset.StudyID = series.study.study_id
    dataset.StudyDescription = series.study.study_description
    dataset.StudyDate = series.study.study_date_time.date()
    dataset.StudyTime = series.study.study_date_time.time()
    dataset.ReferringPhysicianName = series.study.referring_physician_name
    dataset.InstitutionName = series.study.institution_name
    dataset.AccessionNumber = series.study.accession_number
    # TODO: only assign the text representation, without the prefix
    dataset.BodyPartExamined = series.study.anatomic_region

    dataset.SeriesInstanceUID = series.series_uid
    dataset.SOPClassUID = series.sop_class
    dataset.TransferSyntaxUID = series.transfer_syntax
    dataset.SpecificCharacterSet = series.specific_character_set
    dataset.SeriesDate = series.series_datetime.date()
    dataset.SeriesTime = series.series_datetime.time()
    dataset.Modality = series.modality
    dataset.SeriesNumber = series.series_number
    dataset.SeriesDescription = series.series_description
    dataset.SequenceName = series.sequence_name
    dataset.ProtocolName = series.protocol_name
    dataset.SpacingBetweenSlices = series.spacing_between_slices
    dataset.PixelSpacing = pixel_spacing_to_list(series.pixel_spacing)
    dataset.ImageOrientationPatient = vector3d_pair_to_list(series.image_orientation_patient)


class PykkamiManager:
    """
    Interface for pykkami-based applications.
    """

    # region Construction
    def __init__(self):
        self._patient_cache: list[Patient] = []

    # endregion

    # region Properties
    @property
    def patientCache(self):
        return self._patient_cache

    # endregion

    # region Series Creation
    @classmethod
    def create_refurbished_series(cls, study: Study, source_file_names: list[str], metadata: DicomMetadata = None,
                                  initial_image_position_patient: Point3D = (0, 0, 0)) -> Series:
        """
        Creates a "refurbished" series from a number of DICOM files and an instance of DicomMetadata.
        No entries to a database or file system are made. The 'study' value is not assigned.
        :param study: The study in which to create the series.
        :param initial_image_position_patient: Image position for the first image of the series.
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

        instance_number = 0
        for file_name in source_file_names:
            dataset = dicom.read_file(file_name)
            assign_series_data(series, dataset)
            dataset.SOPInstanceUID = DicomUidProvider.create_instance_uid()

            dataset.ImagePositionPatient = [
                initial_image_position_patient[0],
                initial_image_position_patient[1],
                initial_image_position_patient[2] + instance_number * dataset.SpacingBetweenSlices
            ]
            instance_number += 1
            dataset.InstanceNumber = instance_number
            series.instances[dataset.SOPInstanceUID] = dataset

        return series
    # endregion


# The quasi-singleton instance
PykkamiManager_Instance = PykkamiManager()
