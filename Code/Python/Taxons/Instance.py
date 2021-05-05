import pydicom as dicom
import DataTypes
from Taxons import Series
from DicomStuff.DicomUidProvider import DicomUidProvider


class Instance:
    """
    Abstraction of a DICOM instance.
    """
    # region Members
    series: Series = None                                           # The series, owner of the instance
    instance_uid: str = None                                        # Globally unique instance UID
    instance_number: int = 0                                        # DICOM instance number in the series
    instance_position_patient: DataTypes.Point3D = (0, 0, 0)        # DICOM image position in patient as a 3D vector
    dicom_dataset: dicom.dataset = None                             # DICOM dataset.
    # endregion

    # region Construction
    def __init__(self, instance_uid_: str = None):
        """
        Creates an instance of Series.
        :param instance_uid_: The UID of the instance. If set to None (default), an automatic InstanceUID is generated.
        """
        if instance_uid_ is None or len(instance_uid_) < 1:
            self.instance_uid = DicomUidProvider.create_instance_uid()
        else:
            self.instance_uid = instance_uid_
    # endregion

    # region String representation
    def __str__(self):
        """
        String representing the instance.
        :return: The string representation.
        """
        return f"[{self.instance_uid}] ({self.instance_number}). IPP=({self.instance_position_patient[0]}, {self.instance_position_patient[1]}, {self.instance_position_patient[2]})"
    # endregion
