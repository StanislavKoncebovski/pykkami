from datetime import datetime
import random

from DataTypes import PixelSpacing, Vector3DPair
from DicomStuff import DicomConstants
from enumerations import Gender, AnatomicRegion, Modality


class DicomMetadata:
    """
    Contains minimal metadata to create or anonymize a series.
    """
    # region Default values
    _default_sop_class_uid = DicomConstants.VERIFICATION_SOP_CLASS
    _default_transfer_syntax = DicomConstants.DEFAULT_TRANSFER_SYNTAX
    _default_patient_name = "Anonymous^Allain"
    _default_patient_date_of_birth = datetime(1970, 12, 5)
    _default_patient_gender = Gender.Male
    _default_referring_physician_name = "Refery^Roderick"
    _default_institution_name = "Default Dicom Institution"
    _default_accession_number_prefix = "ACN_"
    _default_study_id_prefix = "SID_"
    _default_study_description = "Default Study"
    _default_anatomic_region = AnatomicRegion.EXTREMITY
    _default_modality = Modality.OT
    _default_series_description = "Default Series"
    _default_sequence_name = "Default Sequence"
    _default_protocol_name = "Default Protocol"
    _default_spacing_between_slices = 2.5
    _default_pixel_spacing: PixelSpacing = (1.0, 1.0)
    _default_image_orientation_patient: Vector3DPair = ((1, 0, 0), (0, 1, 0))
    _default_specific_character_set = DicomConstants.DEFAULT_CHARACTER_SET
    # endregion

    def __init__(self):
        self.sop_class_uid = DicomMetadata._default_sop_class_uid
        self.transfer_syntax = DicomMetadata._default_transfer_syntax
        self.specific_character_set = DicomMetadata._default_specific_character_set
        self.patient_name = DicomMetadata._default_patient_name
        self.patient_date_of_birth = DicomMetadata._default_patient_date_of_birth
        self.patient_gender = DicomMetadata._default_patient_gender
        self.referring_physician_name = DicomMetadata._default_referring_physician_name
        self.institution_name = DicomMetadata._default_institution_name
        self.accession_number = f"{DicomMetadata._default_accession_number_prefix}_{random.randint(1000, 10000)}"
        self.study_id = f"{DicomMetadata._default_study_id_prefix}_{random.randint(1000, 10000)}"
        self.study_description = DicomMetadata._default_study_description
        self.modality = DicomMetadata._default_modality
        self.series_description = DicomMetadata._default_study_description
        self.series_number = random.randint(1000, 10000)
        self.sequence_name = DicomMetadata._default_sequence_name
        self.protocol_name = DicomMetadata._default_protocol_name
        self.spacing_between_slices = DicomMetadata._default_spacing_between_slices
        self.pixel_spacing = DicomMetadata._default_pixel_spacing
        self.image_orientation_patient = DicomMetadata._default_image_orientation_patient
