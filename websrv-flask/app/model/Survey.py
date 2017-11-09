from json import JSONDecoder, JSONEncoder

from model.database import PersistentObject


class SurveyEncoder(JSONEncoder): pass


class SurveyDecoder(JSONDecoder): pass


class Survey(PersistentObject):

    def __init__(self, uuid:str):
        super().__init__(uuid)

