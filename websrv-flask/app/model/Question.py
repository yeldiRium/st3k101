from model.database import PersistentObject


class Question(PersistentObject):
    def __init__(self, uuid: str = None):
        super().__init__(uuid)

        self.__text = ""  # type: str
        self.__answer_value = None  # type: int

    @property
    def text(self) -> str:
        return self.__text

    @property
    def answer_value(self) -> int:
        return self.__answer_value

    @text.setter
    def text(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__text", value)

    @answer_value.setter
    def answer_value(self, value: int):
        if type(value) != int:
            raise TypeError
        super().set_member("__answer_value", value)
