from flask_restful import Resource

from api.v2 import api
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


class LanguageResource(Resource):
    def get(self):
        def parse_language(languageEnumItem):
            return {
                'item_id': languageEnumItem.name,
                'value': languageEnumItem.value
            }

        return list(map(parse_language, BabelLanguage))


api.add_resource(LanguageResource, '/api/language')
