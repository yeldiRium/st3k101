from typing import List

from model.PersistentObject import PersistentObject
from model.Question import Question


class QuestionGroup(PersistentObject):
    def __init__(self, uuid: str = None):
        self._name = ""  # type: str
        self._color = "#99ff99"  # type: str
        self._question_ids = None  # type: List[str]

        super().__init__(uuid)


    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> str:
        return self._color

    @property
    def questions(self) -> List[Question]:
        return [Question(uuid) for uuid in self._question_ids]

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_name", value)

    @color.setter
    def color(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_color", value)

    @questions.setter
    def questions(self, value: List[Question]):
        ids = [o.uuid for o in value]
        super().set_member("_question_ids", ids)
