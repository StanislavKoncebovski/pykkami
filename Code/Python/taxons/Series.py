import Study
import Instance
from dicom import DicomConstants
from enumerations import Modality


class Series:
    # region Members
    study: Study = None
    series_uid: str = None

    sop_class: str = DicomConstants.VERIFICATION_SOP_CLASS
    transfer_syntax: str = DicomConstants.DEFAULT_TRANSFER_SYNTAX
    specific_character_set: list[str] = DicomConstants.DEFAULT_CHARACTER_SET
    series_datetime = DicomConstants.MIN_SERIES_DATETIME
    modality: Modality = Modality.Unknown
    series_number: int = 0
    series_description: str = ""
    sequence_name: str = ""
    protocol_name: str = ""
    spacing_between_slices: float = 0.0
    pixel_spacing: (float, float) = (0, 0)
    image_orientation_patient: [(float, float, float), (float, float, float)] = [(1, 0, 0), (0, 1, 0)]
    # endregion

    # region Protected members
    _instances: dict[str, Instance] = {}

    # endregion

    # region Construction
    def __init__(self, series_uid_: str = None):
        if series_uid_ is None or len(series_uid_) < 1:
            self.series_uid = DicomUidProvider.create_series_uid()
        else:
            self.series_uid = series_uid_
    # endregion

    # region Management
    def add_instance(self, instance: Instance):
        if instance.instance_uid not in self._instances.keys():
            instance.series = self
            self._instances[instance.instance_uid] = instance
    # endregion

    # region String representation
    def __str__(self):
        return f"[{self.series_uid}] ({self.series_datetime}). MOD={self.modality}: {self.series_description}"
    # endregion
