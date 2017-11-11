from typing import List

from model.Survey import Survey
from model.database import PersistentObject


class DataClient(PersistentObject):

    def __init__(self, uuid:str=None):
        super().__init__(uuid)

        self.__name = ""  # type: str
        self.__password_salt = ""  # type: str
        self.__password_hash = ""  # type: str
        self.__survey_ids = None  # type: List[str]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def password_salt(self) -> str:
        return self.__password_salt

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    @property
    def surveys(self) -> List[Survey]:
        return [Survey(uuid) for uuid in self.__survey_ids]

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("name", value)

    @password_salt.setter
    def password_salt(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__password_salt", value)

    @password_hash.setter
    def password_hash(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__password_hash", value)

    @surveys.setter
    def surveys(self, value:List[Survey]):
        ids = [o.uuid for o in value]
        super().set_member("__survey_ids", ids)
