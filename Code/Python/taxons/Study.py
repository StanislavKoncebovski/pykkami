from datetime import datetime, date
import Patient
import Series
from dicom import DicomConstants
from dicom.DicomUidProvider import DicomUidProvider
from enumerations import AnatomicRegion, Gender


class Study:
    # region Members
    patient: Patient = None
    study_uid: str = None
    study_date_time: datetime = DicomConstants.MIN_STUDY_DATETIME
    referring_physician_name: str = ""
    institution_name: str = ""
    accession_number: str = ""
    study_id: str = ""
    study_description: str = ""
    anatomic_region: AnatomicRegion = AnatomicRegion.Unknown
    # endregion

    # region Protected members
    _seriez: dict[str, Series] = {}
    # endregion

    # region Construction
    def __init__(self, study_uid_=None):
        if study_uid_ is None or len(study_uid_) < 1:
            self.study_uid = DicomUidProvider.create_study_uid()
        else:
            self.study_uid = study_uid_
    # endregion

    # region Management
    def add_series(self, series: Series):
        if series.series_uid not in self._seriez.keys():
            series.study = self
            self._seriez[series.series_uid] = series
    # endregion

    # region String representation
    def __str__(self):
        return f"[{self.study_uid}] ({self.study_date_time}). ID={self.study_id}: {self.study_description}"
    # endregion


if __name__ == '__main__':
    p1 = Patient.Patient()
    p1.name = "Testmann^Theo"
    p1.date_of_birth = date(1970, 12, 5)
    p1.gender = Gender.Male

    print(p1)

    s1 = Study()
    s1.study_date_time = datetime.now()
    s1.study_id = "S_0001"
    s1.study_description = "Test study"

    print(s1)

    p1.add_study(s1)

    print(p1)