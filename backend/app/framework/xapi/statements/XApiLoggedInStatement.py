from flask import g

from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiActor import XApiMboxActor
from framework.xapi.XApiContext import XApiSt3k101Context
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from model.models.DataClient import DataClient

__author__ = "Noah Hummel"


class XApiLoggedInStatement(XApiStatement):

    def __init__(self, dataclient: DataClient):
        super(XApiLoggedInStatement, self).__init__(
            XApiMboxActor(dataclient.email, dataclient.email),
            XApiVerb(XApiVerbs.LoggedIn),
            XApiActivityObject(
                XApiActivities.Login,
                "http://{}/#/private".format(g._config['DOMAIN_NAME']),  # TODO: replace hard coded url with something more useful
                {
                    "en-US": "St3k101 login view"
                }
            ),
            xapi_context=XApiSt3k101Context()
        )
