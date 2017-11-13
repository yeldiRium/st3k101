from model.PersistentObject import PersistentObject
from model.DataSubject import DataSubject
from model.Question import Question


class QuestionResult(PersistentObject):
    def __init__(self, uuid: str = None):
        self._question_id = ""  # type: str
        self._datasubject_id = ""  # type: str
        self._answer_value = None  # type: int

        super().__init__(uuid)

    @property
    def question(self) -> Question:
        return Question(self._question_id)

    @property
    def datasubject(self) -> DataSubject:
        return DataSubject(self._datasubject_id)

    @property
    def answer_value(self) -> int:
        return self._answer_value

    @question.setter
    def question(self, value: Question):
        super().set_member("_question_id", value.uuid)

    @datasubject.setter
    def datasubject(self, value: DataSubject):
        super().set_member("_datasubject_id", value.uuid)

    @answer_value.setter
    def answer_value(self, value: int):
        if type(value) != int:
            raise TypeError
        super().set_member("_answer_value", value)
