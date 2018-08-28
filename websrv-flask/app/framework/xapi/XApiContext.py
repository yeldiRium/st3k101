from abc import abstractmethod

from XApiItem import XApiItem
from XApiActor import XApiActor


class XApiContext(XApiItem):
    @abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError


class XApiSt3k101Context(XApiContext):
    def __init__(
        self,
        instructor: XApiActor,
        platform: str,
        language: str,
        revision: str
    ):
        self.__instructor = instructor
        self.__platform = platform
        self.__language = language
        self.__revision = revision
    
    def as_dict(self) -> dict:
        return {
            "instructor": self.__instructor,
            "platform": self.__platform,
            "language": self.__language,
            "revision": self.__revision
        }


class XApiSurveyContext(XApiContext):
    def __init__(self, question: "Question"):
        pass