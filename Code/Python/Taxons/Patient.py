from datetime import date
from Taxons import Study
from enumerations import Gender
from DicomStuff.DicomUidProvider import DicomUidProvider


class Patient:
    """
    Abstraction of a patient, according to DICOM
    """
    # region Members
    patient_id: str = None              # Patient ID
    name: str = ""                      # Patient's name, in DICOM notation
    date_of_birth: date = date.min      # Patient's date of birth
    gender: Gender = Gender.Unknown     # Patient's gender
    # endregion

    # region Protected members
    _studies: dict[str, Study] = {}     # Dictionary of patient's studies. Key: StudyUID; Value: the study.
    # endregion

    # region Construction
    def __init__(self, patient_id_=None):
        """
        Creates an instance of Patient.
        :param patient_id_: The ID of the patient. If set to None (default), an automatic PatientID is generated.
        """
        if patient_id_ is None or len(patient_id_) < 1:
            self.patient_id = DicomUidProvider.create_patient_id()
        else:
            self.patient_id = patient_id_
    # endregion

    # region Management
    def add_study(self, study: Study):
        """
        Adds a study to the studies of the patient, if the study_uid is not already present;
        otherwise, nothing happens.
        :param study: The study to add.
        :return: None.
        """
        if study.study_uid not in self._studies.keys():
            study.patient = self
            self._studies[study.study_uid] = study

    # endregion

    # region String representation
    def __str__(self):
        """
        String representing the patient.
        :return: The string representation.
        """
        return f"[{self.patient_id}]: {self.name} ({self.date_of_birth}, {self.gender}). {len(self._studies)} studies"
    # endregion


if __name__ == '__main__':
    p1 = Patient()
    p1.name = "Testmann^Theo"
    p1.date_of_birth = date(1970, 12, 5)
    p1.gender = Gender.Male

    print(p1)
