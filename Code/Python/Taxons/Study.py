from datetime import datetime, date
from DicomStuff import DicomConstants
from DicomStuff.DicomUidProvider import DicomUidProvider
from Taxons import Patient, Series
from enumerations import AnatomicRegion, Gender


class Study:
    """
    Abstraction of a study, according to DICOM.
    """
    # region Members

    study_uid: str = None                                           # Globally unique study UID
    patient: Patient = None  # The patient, owner of the study
    study_date_time: datetime = DicomConstants.MIN_STUDY_DATETIME   # Date/Time of the study
    referring_physician_name: str = ""                              # Name of the referring physician
    institution_name: str = ""                                      # Name of the institution
    accession_number: str = ""                                      # DICOM accession number
    study_id: str = ""                                              # DICOM study ID
    study_description: str = ""                                     # Study description
    anatomic_region: AnatomicRegion = AnatomicRegion.Unknown        # The anatomic region concerned
    # endregion

    # region Protected members
    _seriez: dict[str, Series] = {}                                 # Dictionary of series's to the study. Key: SeriesUID; Value: the series.
    # endregion

    # region Construction
    def __init__(self, study_uid_=None):
        """
        Creates an instance of Study.
        :param study_uid_: The UID of the study. If set to None (default), an automatic StudyUID is generated.
        """
        if study_uid_ is None or len(study_uid_) < 1:
            self.study_uid = DicomUidProvider.create_study_uid()
        else:
            self.study_uid = study_uid_
    # endregion

    # region Validation
    def is_valid(self) -> bool:
        return (self.patient is not None) \
               and self.patient.is_valid() \
               and (self.study_uid is not None) \
               and (len(self.study_uid) > 0)
    # endregion

    # region Management
    def add_series(self, series: Series):
        """
        Adds a series to the series of the study, if the series_uid is not already present;
        otherwise, nothing happens.
        :param series: The series to add.
        :return:
        """
        if series.series_uid not in self._seriez.keys():
            series.study = self
            self._seriez[series.series_uid] = series
    # endregion

    # region String representation
    def __str__(self):
        """
        String representing the study.
        :return: The string representation.
        """
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