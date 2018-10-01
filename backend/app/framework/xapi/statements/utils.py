from auth.session import current_user
from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiActor import XApiAccountActor, XApiMboxActor
from framework.xapi.XApiObject import XApiActivityObject
from model.models.DataClient import DataClient
from model.models.DataSubject import DataSubject
from model.models.Dimension import Dimension
from model.models.Party import Party
from model.models.Question import Question
from model.models.Questionnaire import Questionnaire
from model.models.SurveyBase import SurveyBase

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


def get_questionnaire(the_item: SurveyBase):
    questionnaire = None

    if isinstance(the_item, Question):
        questionnaire = the_item.dimension.questionnaire
    elif isinstance(the_item, Dimension):
        questionnaire = the_item.questionnaire
    elif isinstance(the_item, Questionnaire):
        questionnaire = the_item

    assert questionnaire is not None
    return questionnaire


def get_xapi_target(the_item: SurveyBase) -> str:
    """
    Given a SurveyBase `the_item`, this method returns the xapi target of
    the containing questionnaire.
    :param the_item: {SurveyBase}
    :return: {str}
    """
    return get_questionnaire(the_item).xapi_target


def get_xapi_object(the_item: SurveyBase):
    activity = None
    if isinstance(the_item, Question):
        activity = XApiActivities.Question
    elif isinstance(the_item, Dimension):
        activity = XApiActivities.Dimension
    elif isinstance(the_item, Questionnaire):
        activity = XApiActivities.Questionnaire

    assert activity is not None
    return XApiActivityObject(
        activity,
        "<{}>:{}".format(the_item.owning_dataclient.email, the_item.reference_id),
        the_item.name_translations
    )
