from flask import g

from framework.signals import SIG_LOGGED_IN, SIG_QUESTION_ANSWERED, \
    SIG_ANSWER_VERIFIED, SIG_REFERENCE_ID_UPDATED, SIG_QUESTIONNAIRE_PUBLISHED, SIG_QUESTIONNAIRE_UNPUBLISHED, \
    SIG_SURVEY_CONCLUDED, SIG_LTI_LAUNCH
from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiContext import XApiSt3k101Context
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.XApiPublisher import XApiPublisher
from framework.xapi.XApiResult import XApiResponseResult
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from framework.xapi.statements.XApiAnswerSubmittedStatement import XApiAnswerSubmittedStatement
from framework.xapi.statements.XApiLoggedInStatement import XApiLoggedInStatement
from framework.xapi.statements.utils import get_xapi_target, get_current_user_as_actor, get_xapi_object, \
    get_party_as_actor
from model.models.DataSubject import DataSubject
from model.models.Dimension import Dimension
from model.models.Party import Party
from model.models.Question import Question
from model.models.QuestionResponse import QuestionResponse
from model.models.Questionnaire import Questionnaire
from model.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


@SIG_LOGGED_IN.connect
def publish_logged_in_xapi_statement(sender: Party):
    statement = XApiLoggedInStatement(sender)
    XApiPublisher().enqueue([statement], g._config['XAPI_DEFAULT_ENDPOINT'])


@SIG_LTI_LAUNCH.connect
def publish_lti_launch_xapi_statement(sender: DataSubject, questionnaire=None):
    actor = get_party_as_actor(sender)
    verb = XApiVerb(XApiVerbs.Accessed)
    activity = get_xapi_object(questionnaire)
    context = XApiSt3k101Context()
    statement = XApiStatement(
        actor,
        verb,
        activity,
        xapi_context=context
    )
    XApiPublisher().enqueue([statement], g._config['XAPI_DEFAULT_ENDPOINT'])


@SIG_QUESTION_ANSWERED.connect
def enqueue_answered_xapi_statements(sender: QuestionResponse):
    question = sender.question
    subject = next(filter(lambda s: isinstance(s, DataSubject), sender.owners))
    receiver = get_xapi_target(sender.question)
    statement = XApiAnswerSubmittedStatement(subject, question, sender.value)

    XApiPublisher().enqueue_deferred([statement], receiver, sender.id)


@SIG_ANSWER_VERIFIED.connect
def approve_pending_xapi_statements(sender: QuestionResponse):
    XApiPublisher().approve(sender.id)


@SIG_REFERENCE_ID_UPDATED.connect
def publish_reference_id_updated_xapi_statement(
        sender: SurveyBase,
        previous_value: str="Missing"
):
    actor = get_current_user_as_actor()
    verb = XApiVerb(XApiVerbs.ChangedReferenceId)
    activity = None
    if isinstance(sender, Question):
        activity = XApiActivities.Question
    elif isinstance(sender, Dimension):
        activity = XApiActivities.Dimension
    elif isinstance(sender, Questionnaire):
        activity = XApiActivities.Questionnaire
    assert activity is not None
    previous_value = "<{}>:{}".format(sender.owning_dataclient.email, previous_value)
    activity = XApiActivityObject(activity, previous_value, sender.name_translations)
    result = XApiResponseResult("<{}>:{}".format(sender.owning_dataclient.email, sender.reference_id))
    context = XApiSt3k101Context()

    receiver = get_xapi_target(sender)
    statement = XApiStatement(actor, verb, activity, result, context)
    XApiPublisher().enqueue([statement], receiver)


@SIG_QUESTIONNAIRE_PUBLISHED.connect
def publish_questionnaire_published_xapi_statement(sender: Questionnaire):
    actor = get_current_user_as_actor()
    verb = XApiVerb(XApiVerbs.PublishedSurvey)
    activity = get_xapi_object(sender)
    context = XApiSt3k101Context()

    receiver = get_xapi_target(sender)
    statement = XApiStatement(actor, verb, activity, xapi_context=context)
    XApiPublisher().enqueue([statement], receiver)


@SIG_QUESTIONNAIRE_UNPUBLISHED.connect
def publish_questionnaire_retracted_xapi_statement(sender: Questionnaire):
    actor = get_current_user_as_actor()
    verb = XApiVerb(XApiVerbs.RetractedSurvey)
    activity = get_xapi_object(sender)
    context = XApiSt3k101Context()

    receiver = get_xapi_target(sender)
    statement = XApiStatement(actor, verb, activity, xapi_context=context)
    XApiPublisher().enqueue([statement], receiver)


@SIG_SURVEY_CONCLUDED.connect
def publish_survey_concluded_xapi_statement(sender: Questionnaire):
    actor = get_current_user_as_actor()
    verb = XApiVerb(XApiVerbs.ConcludedSurvey)
    activity = get_xapi_object(sender)
    context = XApiSt3k101Context()

    receiver = get_xapi_object(sender)
    statement = XApiStatement(actor, verb, activity, xapi_context=context)
    XApiPublisher().enqueue([statement], receiver)
