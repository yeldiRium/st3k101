from typing import List

from model.Survey import Survey
from model.PersistentObject import PersistentObject


class DataClient(PersistentObject):

    def __init__(self, uuid:str=None):
        super().__init__(uuid)

        self._email = ""  # type: str
        self._activated = False  # type: bool
        self._password_salt = ""  # type: str
        self._password_hash = ""  # type: str
        self._survey_ids = None  # type: List[str]

    @property
    def email(self) -> str:
        return self._email

    @property
    def activated(self):
        return self._activated

    @property
    def password_salt(self) -> str:
        return self._password_salt

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def surveys(self) -> List[Survey]:
        return [Survey(uuid) for uuid in self._survey_ids]

    @email.setter
    def email(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_email", value)

    @activated.setter
    def activated(self, value: bool):
        if type(value) != bool:
            raise TypeError
        super().set_member("_activated", value)

    @password_salt.setter
    def password_salt(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_password_salt", value)

    @password_hash.setter
    def password_hash(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_password_hash", value)

    @surveys.setter
    def surveys(self, value:List[Survey]):
        ids = [o.uuid for o in value]
        super().set_member("_survey_ids", ids)
