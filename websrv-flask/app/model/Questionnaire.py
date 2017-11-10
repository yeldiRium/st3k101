from typing import List

from model.QuestionGroup import QuestionGroup
from model.database import PersistentObject


class Questionnaire(PersistentObject):

    def __init__(self, uuid:str=None):
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
            raise TypeError
        super().set_member("__name", value)

    @questiongroups.setter
    def questiongroups(self, value:List[QuestionGroup]):
        ids = [o.uuid for o in value]
        super().set_member("__questiongroup_ids", ids)
