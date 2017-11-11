from model.database import PersistentObject


class Question(PersistentObject):
    def __init__(self, uuid: str = None):
        self._text = ""  # type: str

        super().__init__(uuid)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("_text", value)
