from typing import List

from model.Question import Question
from model.database import PersistentObject


class QuestionGroup(PersistentObject):

    def __init__(self, uuid:str):
        super().__init__(uuid)

        self.__name = ""  # type: str
        self.__color = "#99ff99" # type: str
        self.__question_ids = None  # type: List[str]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def questions(self) -> List[Question]:
        return [Question(uuid) for uuid in self.__question_ids]

    @property
    def color(self) -> List[Question]:
        return [Question(uuid) for uuid in self.__question_ids]

    @color.setter
    def color(self, value: str):
        if type(value) != str:
            raise Exception("Invalid type")
        super().set_member("color", value)

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise Exception("Invalid type")
        super().set_member("name", value)

    @questions.setter
    def questions(self, value:List[Question]):
        super().set_member("questions", value)
