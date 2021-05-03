import Study
from datetime import date
from enumerations import Gender
from dicom.DicomUidProvider import DicomUidProvider


class Patient:
    # region Members
    patient_id: str = None
    name: str = ""
    date_of_birth: date = date.min
    gender: Gender = Gender.Unknown
    # endregion

    # region Protected members
    _studies: dict[str, Study] = {}
    # endregion

    # region Construction
    def __init__(self, patient_id_=None):
        if patient_id_ is None or len(patient_id_) < 1:
            self.patient_id = DicomUidProvider.create_patient_id()
        else:
            self.patient_id = patient_id_
    # endregion

    # region Management
    def add_study(self, study: Study):
        """
        Adds a study to the studies of the patients, if the study_uid is not already present;
        otherwise, nothing happens-
        :param study: study to add.
        :return:
        """
        if study.study_uid not in self._studies.keys():
            study.patient = self
            self._studies[study.study_uid] = study

    # endregion

    # region String representation
    def __str__(self):
        return f"[{self.patient_id}]: {self.name} ({self.date_of_birth}, {self.gender}). {len(self._studies)} studies"
    # endregion


if __name__ == '__main__':
    p1 = Patient()
    p1.name = "Testmann^Theo"
    p1.date_of_birth = date(1970, 12, 5)
    p1.gender = Gender.Male

    print(p1)
