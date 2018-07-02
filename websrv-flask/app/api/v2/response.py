from flask import request
from flask_restful import Resource, abort

from api.v2 import api
from api.v2.dependency_injection import ResourceBroker
from api.v2.schema.response import QuestionResponseSchema
from api.v2.schema.submission import SubmissionSchema
from auth.roles import Role, needs_minimum_role
from auth.users import current_user
from framework.captcha import validate_captcha
from model.SQLAlchemy.models.Question import Question
from model.SQLAlchemy.models.QuestionResponse import QuestionResponse
from model.SQLAlchemy.models.Questionnaire import Questionnaire
from utils import generate_verification_token
from utils.dicts import merge_error_dicts
from utils.email import validate_email_blacklist, validate_email_whitelist

__author__ = "Noah Hummel"

def validate_challenges(questionnaire, data):
    errors = dict()
    if questionnaire.password_enabled:
        if 'password' not in data:
            errors['password'] = ['Missing required parameter.']
        elif data['password'] != questionnaire.password:
            errors['password'] = ['Passwords did not match.']

    email = data['data_subject']['email']
    if questionnaire.email_blacklist_enabled:
        if not validate_email_blacklist(questionnaire.email_blacklist, email):
            if 'data_subject' not in errors:
                errors['data_subject'] = dict()
            errors['data_subject']['email'] = ['Email is blacklisted.']
    if questionnaire.email_whitelist_enabled:
        if not validate_email_whitelist(questionnaire.email_whitelist, email):
            if 'data_subject' not in errors:
                errors['data_subject'] = dict()
            errors['data_subject']['email'] = ['Email is not whitelisted.']
    return errors


class ResponseListForQuestionnaireResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        schema = QuestionResponseSchema(many=True)
        responses = []
        for dimension in questionnaire.dimensions:
            for question in dimension.questions:
                responses += question.responses
        return schema.dump(responses)

    def post(self, questionnaire_id: int=None):
        schema = SubmissionSchema()
        data, errors = schema.load(request.json)
        if not validate_captcha(data['captcha_token']):
            return {
                'message': 'CAPTCHA confidence score too low. Please try again.'
            }, 403
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        challenge_errors = validate_challenges(questionnaire, data)
        if challenge_errors:
            return {
               'message': 'Some challenges could not be completed.',
                'errors': merge_error_dicts(errors, challenge_errors)
            }, 403

        verification_token = generate_verification_token()

        for dimension_data in data['dimensions']:
            dimension = next((d for d in questionnaire.dimensions
                              if d.id == dimension_data['id']), None)
            if not dimension:
                return {
                    'message': 'Questionnaire has no dimension with id {}'.format(dimension_data['id'])
                }, 400
            for question_data in dimension_data['questions']:
                question = next((q for q in dimension.questions
                                 if q.id == question_data['id']), None)  # type: Question
                if not question:
                    return {
                        'message': 'Questionnaire has no question with id {}'.format(question_data['id'])
                    }, 400
                question.add_question_result(
                    question_data['value'],
                    data['data_subject']['email'],
                    verification_token=verification_token
                )

        return {
            'message': 'Submission successful. Please verify by email.'
        }, 200

class ResponseListForQuestionResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None, dimension_id: int=None,
            question_id: int=None):
        pass


class ResponseResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None, dimension_id: int=None,
            question_id: int=None, response_id: int=None):
        pass


api.add_resource(
    ResponseListForQuestionnaireResource,
    '/api/questionnaire/<int:questionnaire_id>/response'
)
api.add_resource(
    ResponseListForQuestionResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>/response',
    '/api/dimension/<int:dimension_id>/question/<int:question_id>/response',
    '/api/question/<int:question_id>/response'
)
api.add_resource(
    ResponseResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>/response/<int:response_id>',
    '/api/dimension/<int:dimension_id>/question/<int:question_id>/response/<int:response_id>',
    '/api/question/<int:question_id>/response/<int:response_id>'
)

ResourceBroker.add_resource_for(ResponseResource, QuestionResponse, 'response_id')
