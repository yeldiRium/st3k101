from flask import g

from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiContext import XApiSt3k101Context
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from framework.xapi.statements.utils import get_party_as_actor
from model.models.Party import Party

__author__ = "Noah Hummel"


class XApiLoggedInStatement(XApiStatement):

    def __init__(self, party: Party):
        super(XApiLoggedInStatement, self).__init__(
            get_party_as_actor(party),
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
