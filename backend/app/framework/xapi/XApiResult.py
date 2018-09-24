from abc import abstractmethod

from framework.xapi.XApiItem import XApiItem


class XApiResult(XApiItem):
    @abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError


class XApiScoredResult(XApiResult):
    def __init__(self, score: int, min: int, max: int, step: int):
        self.__raw = score
        self.__min = min
        self.__max = max
        self.__scaled = step

    def as_dict(self) -> dict:
        return {
            "score": {
                "scaled": self.__scaled,
                "min": self.__min,
                "max": self.__max,
                "raw": self.__raw
            }
        }
