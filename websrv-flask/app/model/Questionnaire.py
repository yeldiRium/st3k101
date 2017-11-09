from typing import List

from model.QuestionGroup import QuestionGroup
from model.database import PersistentObject


class Questionnaire(PersistentObject):

    def __init__(self, uuid:str):
        super().__init__(uuid)

        self.__name = ""  # type: str
        self.__questiongroup_ids = None  # type: List[str]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def questiongroups(self) -> List[QuestionGroup]:
        return [QuestionGroup(uuid) for uuid in self.__questiongroup_ids]

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise Exception("Invalid type")
        super().set_member("name", value)

    @questiongroups.setter
    def questiongroups(self, value:List[QuestionGroup]):
        super().set_member("questiongroups", value)
