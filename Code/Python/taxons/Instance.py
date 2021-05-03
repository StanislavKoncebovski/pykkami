import Series
import pydicom as dicom


class Instance:
    # region Members
    series: Series = None
    instance_uid: str = None
    instance_number: int = 0
    instance_position_patient: (float, float, float) = (0, 0, 0)
    dicom_dataset: dicom.dataset = None
    # endregion
