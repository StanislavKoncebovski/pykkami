from DicomStuff import DicomConstants
from Taxons import Study, Instance
from enumerations import Modality
import DataTypes
from DicomStuff.DicomUidProvider import DicomUidProvider


class Series:
    """
    Abstraction of a series, according to DICOM.
    """
    # region Members
    series_uid: str = None                                                      # Globally unique series UID
    study: Study = None                                                         # The study, owner of the series
    sop_class: str = DicomConstants.VERIFICATION_SOP_CLASS                      # SOP Class UID
    transfer_syntax: str = DicomConstants.DEFAULT_TRANSFER_SYNTAX               # Transfer syntax
    specific_character_set: list[str] = DicomConstants.DEFAULT_CHARACTER_SET    # Specific character set
    series_datetime = DicomConstants.MIN_SERIES_DATETIME                        # Date/Time of the series
    modality: Modality = Modality.Unknown                                       # Modality of the series
    series_number: int = 0                                                      # DICOM series number
    series_description: str = ""                                                # Series description
    sequence_name: str = ""                                                     # Name of the DICOM sequence
    protocol_name: str = ""                                                     # Name of the acquisition protocol
    spacing_between_slices: float = 0.0                                         # Spacing between slices
    pixel_spacing: DataTypes.PixelSpacing = (0, 0)                              # Pixel spacing: mm/pix: (rows, columns)
    image_orientation_patient: DataTypes.Vector3DPair = [(1, 0, 0),
                                                         (0, 1, 0)]  # DICOM image orientation in patient vector pair
    # endregion

    # region Protected members
    _instances: dict[str, Instance] = {}                                         # Dictionary of instances to the series. Key: InstanceUID; Value: the instance.
    # endregion

    # region Construction
    def __init__(self, series_uid_: str = None):
        """
        Creates an instance of Series.
        :param series_uid_: The UID of the series. If set to None (default), an automatic SeriesUID is generated.
        """
        if series_uid_ is None or len(series_uid_) < 1:
            self.series_uid = DicomUidProvider.create_series_uid()
        else:
            self.series_uid = series_uid_
    # endregion

    # region Management
    def add_instance(self, instance: Instance):
        """
        Adds an instance to the series, if the instance_uid is not already present;
        otherwise, nothing happens.
        :param instance:  The instance to add.
        :return: None.
        """
        if instance.instance_uid not in self._instances.keys():
            instance.series = self
            self._instances[instance.instance_uid] = instance
    # endregion

    # region String representation
    def __str__(self):
        """
        String representing the series.
        :return: The string representation.
        """
        return f"[{self.series_uid}] ({self.series_datetime}). MOD={self.modality}: {self.series_description}"
    # endregion
