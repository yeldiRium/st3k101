import json

from framework.xapi.XApiItem import XApiItem
from framework.xapi.XApiVerbs import XApiVerbs

class XApiVerb(XApiItem):
    
    def __init__(self, verb: XApiVerbs):
        self.__id = verb.value["id"]
        self.__display = verb.value["display"]

    def get_id(self) -> str:
        return self.__id

    def get_display(self) -> dict:
        """
        Returns an internationalized version of the Verb's name as a dictionary.
        Language tags according to RFC 5646 are used as keys.
        For a list of supported languages, see framework/internationalization/babel_languages.
        """
        return self.__display

    def as_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "display": self.get_display()
        }
