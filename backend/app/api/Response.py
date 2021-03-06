from typing import List

import csv
from io import StringIO

from smtplib import SMTPRecipientsRefused, SMTPHeloError, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError

from flask import request, Response
from flask_restful import Resource, abort

from api import api
from api.utils.ResourceBroker import ResourceBroker
from api.schema.Response import QuestionResponseSchema
from api.schema.Submission import SubmissionSchema
from auth.roles import Role, needs_minimum_role
from auth.session import current_user
from framework.captcha import validate_captcha
from framework.internationalization import _
from framework.signals import SIG_ANSWER_VERIFIED
from framework.xapi.XApiPublisher import XApiPublisher
from framework.xapi.submission_hooks import do_submission_hooks
from framework import make_error
from model import db
from model.models.DataSubject import DataSubject
from model.models.Dimension import Dimension
from model.models.Question import Question
from model.models.QuestionResponse import QuestionResponse
from model.models.Questionnaire import Questionnaire
from utils import generate_verification_token
from framework.email import validate_email_blacklist, validate_email_whitelist, construct_verification_email, send_mail

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


def validate_resource_path(
        questionnaire_id=None,
        dimension_id=None,
        question_id=None
):
    questionnaire = None
    dimension = None
    question = None
    if questionnaire_id is not None:
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
    if dimension_id is not None:
        dimension = Dimension.query.get_or_404(dimension_id)
    if question_id is not None:
        question = Question.query.get_or_404(question_id)

    if question is not None and dimension is not None:
        if question.dimension_id != dimension_id:
            abort(404)
    if dimension is not None and questionnaire is not None:
        if dimension.questionnaire != questionnaire:
            abort(404)
    if questionnaire is not None and question is not None:
        if dimension is None:
            abort(400)
    return questionnaire, dimension, question


class ResponseListForQuestionnaireResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int = None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        output_format = request.args.get('format', default='json')
        if not questionnaire.accessible_by(current_user()):
            abort(403)
        schema = QuestionResponseSchema(many=True)
        responses = []
        for dimension in questionnaire.dimensions:
            for question in dimension.questions:
                responses += question.responses
        if output_format == 'json':
            return schema.dump(responses).data
        elif output_format == 'csv':
            buffer = StringIO()
            writer = csv.writer(buffer)
            writer.writerow(
                [
                    'value',
                    'data_subject',
                    'question_id',
                    'question_text',
                    'range_start',
                    'range_end',
                    'range_start_label',
                    'range_end_label',
                    'dimension_randomized',
                    'dimension_name',
                    'dimension_id'
                ]
            )
            for response in responses:
                writer.writerow(
                    [
                        response.value,
                        schema.anonymize_data_client(response),
                        response.question.reference_id,
                        response.question.text,
                        response.question.range_start,
                        response.question.range_end,
                        response.question.range_start_label,
                        response.question.range_end_label,
                        response.question.dimension.randomize_question_order,
                        response.question.dimension.name,
                        response.question.dimension.reference_id
                    ]
                )
            return Response(buffer.getvalue(), mimetype='text/csv')
        else:
            return make_error('Unrecognized format. Allowed values are: json, csv', 400)

    def post(self, questionnaire_id: int = None):
        schema = SubmissionSchema()
        data, errors = schema.load(request.json)
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)

        if errors:
            return {
                'message': 'Your request contained errors.',
                'errors': errors
            }, 400

        # survey lifecycle check
        if not questionnaire.published:
            abort(403)
        if not questionnaire.accepts_submissions:
            abort(403, message="Submissions are not accepted at this point")

        # captcha and challenges
        if not validate_captcha(data['captcha_token']):
            return {
                'message': 'CAPTCHA confidence score too low. Please try again.'
            }, 403
        challenge_errors = validate_challenges(questionnaire, data)
        if challenge_errors:
            return {
                'message': 'Some challenges could not be completed.',
                'errors': challenge_errors
            }, 403

        verification_token = generate_verification_token()
        data_subject = DataSubject.get_or_create(data['data_subject']['email'])

        all_questions = {
            q.id for d in questionnaire.dimensions for q in d.questions}

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
                question.add_question_result(question_data['value'], data_subject,
                                             verification_token=verification_token)

                all_questions.remove(question_data['id'])

            do_submission_hooks(dimension, dimension_data, data_subject)

        do_submission_hooks(questionnaire, data, data_subject)

        if all_questions:
            db.session.rollback()
            XApiPublisher().rollback()
            return {
                'message': 'Missing questions.',
                'missing': list(all_questions)
            }, 400

        try:
            send_mail(
                data_subject.email,
                _("Please verify your survey submission"),
                construct_verification_email(questionnaire, verification_token)
            )
        except (
            SMTPRecipientsRefused,
            SMTPHeloError,
            SMTPSenderRefused,
            SMTPDataError,
            SMTPNotSupportedError,
            OSError
        ) as e:
            db.session.rollback()
            XApiPublisher().rollback()
            return {
                'message': 'Error while sending verification email.',
                'errors': [str(e)]
            }, 500

        db.session.commit()
        return {
            'message': 'Submission successful. Please verify by email.'
        }, 200


class ResponseListForQuestionResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int = None, dimension_id: int = None,
            question_id: int = None):
        _, _, question = validate_resource_path(questionnaire_id, dimension_id,
                                                question_id)
        if question is None:
            abort(404)
        if not question.accessible_by(current_user()):
            abort(403)
        schema = QuestionResponseSchema(many=True)
        return schema.dump(question.responses).data


class ResponseResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int = None, dimension_id: int = None,
            question_id: int = None, response_id: int = None):
        _, _, question = validate_resource_path(questionnaire_id, dimension_id,
                                                question_id)
        response = QuestionResponse.query.get_or_404(response_id)
        if question is not None:
            if response.question_id != question.id:
                abort(404)
        if not response.accessible_by(current_user()):
            abort(403)
        return QuestionResponseSchema().dump(response).data


class ResponseVerificationResource(Resource):
    def get(self, verification_token: str = None):
        responses = QuestionResponse.query.filter_by(
            verification_token=verification_token).all()  # type: List[QuestionResponse]
        if not responses:
            abort(404)
        for response in responses:
            response.verify()
            response.question.statistic.update()
            SIG_ANSWER_VERIFIED.send(response)

        db.session.commit()
        return _("Your answers have been saved. Thank you for participating!")


class LtiResponseResource(Resource):
    @needs_minimum_role(Role.Unprivileged)
    def post(self, questionnaire_id: int = None):
        schema = SubmissionSchema(exclude=["data_subject"])
        data, errors = schema.load(request.json)
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)

        if errors:
            return {
                'message': 'Your request contained errors.',
                'errors': errors
            }, 400

        # survey lifecycle check
        if not questionnaire.published:
            abort(403, message="Survey was not published yet.")
        if not questionnaire.allow_embedded:
            abort(403)
        if not questionnaire.accepts_submissions:
            abort(403, message="Submissions are not accepted at this point.")

        all_questions = {
            q.id for d in questionnaire.dimensions for q in d.questions}
        responses = []

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

                responses.append(question.add_question_result(
                    question_data['value'],
                    current_user(),
                    needs_verification=False
                ))
                all_questions.remove(question_data['id'])
                question.statistic.update()

            do_submission_hooks(dimension, dimension_data)

        do_submission_hooks(questionnaire, data)

        if all_questions:
            db.session.rollback()
            XApiPublisher().rollback()
            return {
                'message': 'Missing questions.',
                'missing': list(all_questions)
            }, 400

        for response in responses:
            SIG_ANSWER_VERIFIED.send(response)
        db.session.commit()
        return {
            'message': 'Submission successful.'
        }, 200


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
    '/api/response/<int:response_id>'
)

api.add_resource(
    ResponseVerificationResource,
    '/api/response/verify/<verification_token>'
)

api.add_resource(
    LtiResponseResource,
    '/api/questionnaire/<int:questionnaire_id>/lti/response'
)

ResourceBroker.add_resource_for(
    ResponseResource, QuestionResponse, 'response_id')
