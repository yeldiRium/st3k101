from model.database import PersistentObject


class Question(PersistentObject):
    def __init__(self, uuid: str = None):
        self._text = ""  # type: str
        self._answer_value = None  # type: int

        super().__init__(uuid)

    @property
    def text(self) -> str:
        return self._text

    @property
    def answer_value(self) -> int:
        return self._answer_value

    @text.setter
    def text(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_text", value)

    @answer_value.setter
    def answer_value(self, value: int):
        if type(value) != int:
            raise TypeError
        super().set_member("_answer_value", value)
