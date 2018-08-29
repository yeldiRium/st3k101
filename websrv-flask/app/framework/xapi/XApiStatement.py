from framework.xapi.XApiItem import XApiItem
from framework.xapi.XApiActor import XApiActor
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiObject import XApiObject
from framework.xapi.XApiResult import XApiResult
from framework.xapi.XApiContext import XApiContext


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

    def get_actor(self) -> XApiActor:
        return self.__actor

    def get_verb(self) -> XApiVerb:
        return self.__verb

    def get_object(self) -> XApiObject:
        return self.__object

    def get_result(self) -> XApiResult:
        return self.__result

    def get_context(self) -> XApiContext:
        return self.__context

    def as_dict(self) -> dict:
        me = {
            # "timestamp": datetime.now().isoformat(), TODO: manage this by XApiPublisher
            "id": "FIXME: generate unique IDs",  # FIXME: manage this by XApiPublisher
            "actor": self.get_actor().as_dict(),
            "verb": self.get_verb().as_dict(),
            "object": self.get_object().as_dict()
        }

        if self.get_result() is not None:
            me["result"] = self.__result.as_dict(),
        if self.get_context() is not None:
            me["context"] = self.__context.as_dict()

        return me
