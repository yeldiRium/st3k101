from model.database import PersistentObject
from model.Questionnaire import Questionnaire


class Survey(PersistentObject):

    def __init__(self, uuid:str=None):
        super().__init__(uuid)

        self.__name = ""  # type: str
        self.__questionnaire_ids = None  # type: List[str]
        self.__date_created = ""  # type: str

    @property
    def name(self) -> str:
        return self.__name

    @property
    def questionnaires(self) -> List[Questionnaire]:
        return [Questionnaire(uuid) for uuid in self.__questionnaire_ids]

    @name.setter
    def name(self, value: str):
        if type(value) != str:
            raise TypeError
        super().set_member("__name", value)

    @questionnaires.setter
    def questionnaires(self, value:List[Questionnaire]):
        ids = [o.uuid for o in value]
        super().set_member("__questionnaire_ids", ids)


