from abc import abstractmethod

from flask import g
from geolite2 import geolite2

from auth.session import current_user
from framework import get_client_ip
from api.utils.ResourceBroker import ResourceBroker
from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiItem import XApiItem
from framework.xapi.XApiActor import XApiMboxActor
from framework.xapi.XApiObject import XApiActivityObject
from model.models.DataSubject import DataSubject


class XApiContext(XApiItem):
    @abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError


class XApiSt3k101Context(XApiContext):
    """
    Provides the default context for all xAPI statements issued by st3k101.
    It includes a platform string, containing the name "st3k101" as well
    as the tool consumer guid if the statement was generated via an embedded context,
    the request language and, if available, the client's geolocation.
    """
    def __init__(self):
        self.__platform = "st3k101"
        if current_user() and isinstance(current_user(), DataSubject):
            self.__platform += " via {}".format(current_user().source)

        self.__language = g._language.name

        try:
            location = geolite2.reader().get(get_client_ip())["location"]
            self.__geolocation = (location["latitude"], location["longitude"])
        except (ValueError, TypeError):
            self.__geolocation = None
    
    def as_dict(self) -> dict:
        me = {
            "platform": self.__platform,
            "language": self.__language
        }

        if self.__geolocation is not None:
            me["extensions"] = {
                "http://activitystrea.ms/schema/1.0/place": {
                    "definition": {
                        "type": "http://activitystrea.ms/schema/1.0/place",
                        "name": {
                            "en-US": "Place"
                        },
                        "description": {
                            "en-US": "Represents a physical location."
                        }
                    },
                    "id": "http://vocab.org/placetime/geopoint/wgs84/X{}Y{}.html".format(*self.__geolocation),
                    "geojson": {
                        "type": "FeatureCollection",
                        "features": [{
                            "geometry": {
                                "type": "Point",
                                "coordinates": [*self.__geolocation]
                            },
                            "type": "Feature"
                        }]
                    },
                    "objectType": "Place"
                }
            }
        return me


class XApiSurveyContext(XApiContext):
    def __init__(self, question: "Question"):
        first_owner = next((o for o in question.owners))
        super(XApiSurveyContext, self).__init__()
        self.__instructor = XApiMboxActor(first_owner.email, first_owner.email)
        self.__question = question

    def as_dict(self) -> dict:
        return {
            "instructor": self.__instructor.as_dict(),
            "contextActivities": {
                "parent": [
                    XApiActivityObject(
                        XApiActivities.Dimension,
                        ResourceBroker.url_for(self.__question.dimension),
                        self.__question.dimension.name_translations
                    )
                ],
                "grouping": [
                    XApiActivityObject(
                        XApiActivities.Questionnaire,
                        ResourceBroker.url_for(self.__question.dimension.questionnaire),
                        self.__question.dimension.questionnaire.name_translations
                    )
                ]
            },
            **super(XApiSurveyContext, self).as_dict()
        }
