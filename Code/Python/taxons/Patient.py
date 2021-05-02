from Taxon import Taxon
from datetime import date
from enumerations import Gender


class Patient(Taxon):
    # region Protected Members
    _name: str = ""
    _date_of_birth: date = date.min
    _gender: Gender = Gender.Unknown
    # endregion

    # region Construction
    def __init__(self):
        pass
    # endregion

    # region Properties
    @property
    def name(self) -> str:
        return self._name

    @property
    def date_of_birth(self) -> date:
        return self._date_of_birth

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def patient_id(self) -> str:
        return super().uid

    @name.setter
    def name(self, value: str):
        self._name = value

    @date_of_birth.setter
    def date_of_birth(self, value: date):
        self._date_of_birth = value

    @gender.setter
    def gender(self, value: Gender):
        self._gender = value

    @patient_id.setter
    def patient_id(self, value: str):
        self.uid = value
    # endregion

    # region String representation
    def __str__(self):
        return f"[{self.uid}]: {self._name} ({self._date_of_birth}, {self._gender})"
    # endregion


if __name__ == '__main__':
    p1 = Patient()
    p1.name = "Testmann^Theo"
    p1.patient_id = "1007.87621"
    p1.date_of_birth = date(1970, 12, 5)
    p1.gender = Gender.Male


    print(p1)
