from abc import abstractmethod

from flask import g
from geolite2 import geolite2

from auth.session import current_user
from framework import get_client_ip
from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiItem import XApiItem
from framework.xapi.XApiActor import XApiMboxActor
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.statements.utils import get_xapi_object
from model.models.DataSubject import DataSubject


class XApiContext(XApiItem):
    @abstractmethod
    def as_dict(self) -> dict:
        raise NotImplementedError


class XApiSt3k101Context(XApiContext):
    """
    Provides the base context for all xAPI statements issued by st3k101.
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
            ip = get_client_ip() if not g._config['DEBUG_SPOOF_LOCATION'] else "141.2.1.21"
            location = geolite2.reader().get(ip)["location"]
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


class XApiSurveyContext(XApiSt3k101Context):
    def __init__(self, survey_base):
        first_owner = survey_base.owning_dataclient
        super(XApiSurveyContext, self).__init__()
        self.__owning_dataclient = XApiMboxActor(first_owner.email, first_owner.email)
        self.__survey_base = survey_base

    def as_dict(self) -> dict:
        me = super(XApiSurveyContext, self).as_dict()

        context_activities = dict()
        from model.models.Dimension import Dimension
        from model.models.Question import Question
        if isinstance(self.__survey_base, Dimension):
            context_activities['parent'] = [
                get_xapi_object(self.__survey_base.questionnaire).as_dict()
            ]
        elif isinstance(self.__survey_base, Question):
            context_activities['parent'] = [
                get_xapi_object(self.__survey_base.dimension).as_dict()
            ]
            context_activities['grouping'] = [
                get_xapi_object(self.__survey_base.dimension.questionnaire).as_dict()
            ]
        if context_activities:
            me['contextActivities'] = context_activities

        return me
