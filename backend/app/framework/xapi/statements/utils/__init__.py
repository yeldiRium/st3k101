from auth.session import current_user
from framework.xapi.XApiActor import XApiAccountActor, XApiMboxActor
from model.models.DataClient import DataClient
from model.models.DataSubject import DataSubject
from model.models.Party import Party

__author__ = "Noah Hummel"


def get_party_as_actor(party: Party):
    if isinstance(party, DataSubject):
        username = party.moodle_username if party.moodle_username else party.lti_user_id
        actor = XApiAccountActor(username, username, party.source)
    elif isinstance(party, DataClient):
        actor = XApiMboxActor(party.email, party.email)
    else:
        actor = None

    assert actor is not None
    return actor


def get_current_user_as_actor():
    """
    To be used within a request context.
    :return: the currently logged in user a an XApiActor.
    """
    return get_party_as_actor(current_user())
