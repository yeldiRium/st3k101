from datetime import datetime 

from XApiItem import XApiItem
from XApiActor import XApiActor
from XApiVerb import XApiVerb
from XApiObject import XApiObject
from XApiResult import XApiResult
from XApiContext import XApiContext


class XApiStatement(XApiItem):
    def __init__(
        self,
        xapi_actor: XApiActor,
        xapi_verb: XApiVerb,
        xapi_object: XApiObject,
        xapi_result: XApiResult=None,
        xapi_context: XApiContext=None
    ):
        self.__actor = xapi_actor
        self.__verb = xapi_verb
        self.__object = xapi_object
        self.__result = xapi_result
        self.__context = xapi_context

    def as_dict(self) -> dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "id": "FIXME: generate unique IDs",  # FIXME
            "actor": self.__actor.as_dict(),
            "verb": self.__verb.as_dict(),
            "object": self.__object.as_dict(),
            "result": self.__result.as_dict(),
            "context": self.__context.as_dict()
        }