from abc import abstractmethod

from XApiItem import XApiItem
from XApiActivities import XApiActivities
from XApiActor import XApiActor


class XApiObject(XApiItem):

    @abstractmethod
    def get_object_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_object_info(self) -> dict:
        raise NotImplementedError

    def as_dict(self) -> dict:
        return {
            "objectType": self.get_object_type(),
            **self.get_object_info()
        }


class XApiActivityObject(XApiObject):

    def __init__(self, activity: XApiActivities, activity_id: str, activity_name: dict):
        self.__activity_type = activity.value["type"]
        self.__activity_description = activity.value["description"]
        self.__id = activity_id
        self.__name = activity_name

    def get_object_type(self) -> str:
        return "Activity"

    def get_id(self) -> str:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name

    def get_activity_type(self) -> str:
        return self.__activity_type

    def get_activity_description(self) -> dict:
        return self.__activity_description

    def get_object_info(self) -> dict:
        return {
            "id": self.get_id(),
            "definition": {
                "name": self.get_name(),
                "description": self.get_activity_description(),
                "type": self.get_activity_type()
            }
        }

class XApiAgentObject(XApiObject):

    def __init__(self, agent: XApiActor):
        self.__agent = agent

    def get_agent(self) -> XApiActor:
        return self.__agent

    def get_object_type(self) -> str:
        return "Agent"

    def get_object_info(self) -> dict:
        return self.get_agent().as_dict()


class xApiStatementRefObject(XApiObject):

    def __init__(self, statement: "XApiStatement"):
        self.__statement = statement

    def get_statement(self) -> "XApiStatement":
        return self.__statement

    def get_object_type(self) -> str:
        return "StatementRef"

    def get_object_info(self) -> dict:
        return {
            "id": self.get_statement().get_id()
        }
