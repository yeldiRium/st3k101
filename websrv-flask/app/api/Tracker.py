from flask_restful import Resource, abort

from api import api
from api.schema.TrackerEntry import serialize_mixed_list, TRACKER_ENTRY_MAPPING
from auth.roles import needs_minimum_role, Role
from auth.users import current_user
from model.models.DataClient import DataClient
from model.models.Dimension import Dimension
from model.models.OwnershipBase import query_owned
from model.models.Question import Question
from model.models.Questionnaire import Questionnaire
from model.models.TrackerEntry import TrackerEntry

__author__ = "Noah Hummel"


class TrackerResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self):
        entries = query_owned(DataClient, current_user().id, TrackerEntry).all()
        return serialize_mixed_list(entries, TRACKER_ENTRY_MAPPING)


def tracker_entries_for_survey_base(survey_base):
    tracker_entry_types = [
        'property_updated_tracker_entries',
        'translated_property_updated_tracker_entry',
        'item_added_parent_tracker_entries',
        'item_removed_parent_tracker_entries'
    ]
    tracker_entries = []
    for tet in tracker_entry_types:
        es = getattr(survey_base, tet, [])
        tracker_entries += es
    return tracker_entries


class QuestionnaireTrackerResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        tracker_entries = tracker_entries_for_survey_base(questionnaire)
        return serialize_mixed_list(tracker_entries, TRACKER_ENTRY_MAPPING)


class DimensionTrackerResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None, dimension_id: int=None):
        dimension = Dimension.query.get_or_404(dimension_id)
        if questionnaire_id is not None:
            if questionnaire_id != dimension.questionnaire_id:
                abort(404)
        if not dimension.accessible_by(current_user()):
            abort(404)
        tracker_entries = tracker_entries_for_survey_base(dimension)
        return serialize_mixed_list(tracker_entries, TRACKER_ENTRY_MAPPING)


class QuestionTrackerResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None, dimension_id: int=None,
            question_id: int=None):
        question = Question.query.get_or_404(question_id)
        if dimension_id is not None:
            if question.dimension_id != dimension_id:
                abort(404)
        if questionnaire_id is not None:
            if questionnaire_id != question.dimension.questionnaire_id:
                abort(404)
        if not question.accessible_by(current_user()):
            abort(404)
        tracker_entries = tracker_entries_for_survey_base(question)
        return serialize_mixed_list(tracker_entries, TRACKER_ENTRY_MAPPING)


api.add_resource(
    TrackerResource,
    '/api/tracker'
)

api.add_resource(
    QuestionnaireTrackerResource,
    '/api/questionnaire/<int:questionnaire_id>/tracker'
)

api.add_resource(
    DimensionTrackerResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/tracker',
    '/api/dimension/<int:dimension_id>/tracker'
)

api.add_resource(
    QuestionTrackerResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>/tracker',
    '/api/dimension/<int:dimensions_id>/question/<int:question_id>/tracker',
    '/api/question/<int:question_id>/tracker'
)