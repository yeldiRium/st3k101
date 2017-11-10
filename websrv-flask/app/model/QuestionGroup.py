from typing import List

from model.database import PersistentObject
from model.Question import Question


class QuestionGroup(PersistentObject):
    def __init__(self, uuid: str = None):
        super().__init__(uuid)

        self.__name = ""  # type: str
        self.__color = "#99ff99"  # type: str
        self.__question_ids = None  # type: List[str]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def color(self) -> str:
        return self.__color

    @property
    def questions(self) -> List[Question]:
        return [Question(uuid) for uuid in self.__question_ids]

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__name", value)

    @color.setter
    def color(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__color", value)

    @questions.setter
    def questions(self, value: List[Question]):
        ids = [o.uuid for o in value]
        super().set_member("__question_ids", ids)
