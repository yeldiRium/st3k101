from model.database import PersistentObject


class Question(PersistentObject):

    def __init__(self, uuid:str):
        super().__init__(uuid)

        self.__text = ""  # type: str
        self.__answer_value = None  # type: int

    @property
    def text(self) -> str:
        return self.__text

    @property
    def value(self) -> int:
        return self.__answer_value

    @text.setter
    def text(self, value: str):
        if type(value) != str:
            raise Exception("Invalid type")
        super().set_member("text", value)

    @value.setter
    def value(self, value:int):
        if type(value) != int:
            raise Exception("Invalid type")
        super().set_member("value", value)
