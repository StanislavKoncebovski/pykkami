import datetime
from random import randrange
import DicomStuff.DicomConstants


class DicomUidProvider:
    _infix_study: str = "2"
    _infix_series: str = "3"
    _infix_instance: str = "4"
    _min_patient_id: int = 10_000_000_000_000
    _max_patient_id: int = 10_000_000_000_000_000
    _max_random_component: int = 10000

    @classmethod
    def create_patient_id(cls) -> str:
        return str(randrange(cls._min_patient_id, cls._max_patient_id))

    @classmethod
    def create_study_uid(cls) -> str:
        return cls.create_uid(cls._infix_study)

    @classmethod
    def create_series_uid(cls) -> str:
        return cls.create_uid(cls._infix_series)

    @classmethod
    def create_instance_uid(cls) -> str:
        return cls.create_uid(cls._infix_instance)

    # region Private methods
    @classmethod
    def create_uid(cls, infix: str) -> str:
        # the random component of the uid
        random = f"{randrange(1, cls._max_random_component)}"
        return f'{DicomStuff.DicomConstants.DICOM_ROOT}.{infix}.{datetime.datetime.now().strftime("%Y%M%d%H%M%S.%f")[:-3]}.{random}'
    # endregion
