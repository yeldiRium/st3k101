from typing import List

from model.PersistentObject import PersistentObject
from model.Questionnaire import Questionnaire


class Survey(PersistentObject):
    def __init__(self, uuid: str = None):
        self.__name = ""  # type: str
        self.__questionnaire_ids = None  # type: List[str]
        self.__date_created = ""  # type: str

        super().__init__(uuid)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def questionnaires(self) -> List[Questionnaire]:
        return [Questionnaire(uuid) for uuid in self.__questionnaire_ids]

    @property
    def date_created(self):
        return

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__name", value)

    @questionnaires.setter
    def questionnaires(self, value: List[Questionnaire]):
        ids = [o.uuid for o in value]
        super().set_member("__questionnaire_ids", ids)
