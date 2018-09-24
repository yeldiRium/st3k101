from flask import g

from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiActor import XApiMboxActor, XApiAccountActor
from framework.xapi.XApiContext import XApiSt3k101Context
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from model.models.DataSubject import DataSubject
from model.models.Party import Party

__author__ = "Noah Hummel"


class XApiLoggedInStatement(XApiStatement):

    def __init__(self, party: Party):
        if isinstance(party, DataSubject):
            username = party.moodle_username if party.moodle_username else party.lti_user_id
            actor = XApiAccountActor(username, username, party.source)
        else:
            actor = XApiMboxActor(party.email, party.email)

        super(XApiLoggedInStatement, self).__init__(
            actor,
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
