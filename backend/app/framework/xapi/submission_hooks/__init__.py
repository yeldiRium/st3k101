import re

from framework.xapi.XApiContext import XApiSurveyContext
from framework.xapi.XApiResult import XApiScoredResult
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from framework.xapi.XApiPublisher import XApiPublisher
from framework.xapi.statements.utils import get_xapi_target, get_current_user_as_actor, get_xapi_object, \
    get_questionnaire, get_party_as_actor
from framework.xapi.submission_hooks.scoring_strategies.AverageQuestionsInDimension import AverageQuestionsInDimension
from framework.xapi.submission_hooks.hooks import hooks
from model.models.Party import Party
from model.models.Question import Question
from model.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


def get_hook_configuration(the_item: SurveyBase):
    for key, config in hooks.items():
        if key.startswith('regex:'):
            pattern = re.compile(key.replace('regex:', ''))
            if re.match(pattern, the_item.reference_id):
                return config
        else:
            if key == the_item.reference_id:
                return config


def do_submission_hooks(the_item: SurveyBase, submission_data: dict, actor: Party=None):
    assert not isinstance(the_item, Question)  # no submission hooks for single questions

    hook_configuration = get_hook_configuration(the_item)
    if hook_configuration is None:
        return

    score = hook_configuration['scoring_strategy'].score_item(submission_data)

    actor = get_current_user_as_actor() if actor is None else get_party_as_actor(actor)
    verb = XApiVerb(XApiVerbs.Answered)
    activity = get_xapi_object(the_item)
    result = XApiScoredResult(
        score,
        hook_configuration['score_min'],
        hook_configuration['score_max'],
        1
    )
    context = XApiSurveyContext(the_item)

    statement = XApiStatement(
        actor,
        verb,
        activity,
        result,
        context
    )

    questionnaire = get_questionnaire(the_item)
    XApiPublisher().enqueue_deferred([statement], [get_xapi_target(the_item)], questionnaire.id)
