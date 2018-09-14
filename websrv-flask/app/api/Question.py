from flask import request
from flask_restful import Resource, abort

from api import api
from framework.dependency_injection import ResourceBroker
from api.schema.Question import QuestionSchema, ShadowQuestionSchema
from auth.roles import needs_minimum_role, Role, current_has_minimum_role
from auth.session import current_user
from model import db
from model.models.Dimension import Dimension
from model.models.Question import Question, ShadowQuestion

__author__ = "Noah Hummel"


class QuestionResource(Resource):
    @staticmethod
    def get_question_or_404(questionnaire_id=None, dimension_id=None,
                            question_id=None):
        question = Question.query.get_or_404(question_id)  # type: Question
        if dimension_id is not None:
            if question.dimension_id != dimension_id:
                abort(404)
        if questionnaire_id is not None:
            if question.dimension.questionnaire_id != questionnaire_id:
                abort(404)

        return question

    def get(self, questionnaire_id=None, dimension_id=None, question_id=None):
        question = self.get_question_or_404(questionnaire_id, dimension_id,
                                            question_id)
        if not question.accessible_by(current_user()):
            abort(403)

        return QuestionSchema().dump(question).data

    @needs_minimum_role(Role.User)
    def patch(self, questionnaire_id=None, dimension_id=None, question_id=None):
        question = self.get_question_or_404(questionnaire_id, dimension_id,
                                            question_id)
        if not question.accessible_by(current_user()):
            abort(403)
        if not question.modifiable_by(current_user()):
            abort(403)

        schema = QuestionSchema()
        data, errors = schema.load(request.json, partial=True)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'Question not updated. Some errors occurred.',
                'errors': errors
            }, 400

        if isinstance(question, ShadowQuestion):
            abort(403)

        for k, v in data.items():
            if 'k' == 'template':
                if not current_has_minimum_role(Role.Contributor):
                    errors[k] = ['You need to be a contributor to publish '
                                 'templates.']
                    continue
            setattr(question, k, v)
        db.session.commit()

        response = {
            'message': 'Question updated.',
            'question': schema.dump(question).data
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response

    @needs_minimum_role(Role.User)
    def delete(self, **kwargs):
        question = self.get_question_or_404(**kwargs)
        if not question.accessible_by(current_user()):
            abort(403)
        if not question.modifiable_by(current_user()):
            abort(403)
        data = QuestionSchema().dump(question).data
        question.dimension.remove_question(question)
        db.session.commit()
        return {
            'message': 'Question removed.',
            'question': data
        }


class ConcreteQuestionResource(Resource):
    @needs_minimum_role(Role.User)
    def post(self, questionnaire_id: int=None, dimension_id: int=None):
        schema = QuestionSchema()
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'Question not created. Some errors occurred.',
                'errors': errors
            }, 400

        dimension = Dimension.query.get_or_404(dimension_id)
        if questionnaire_id is not None:
            if dimension.questionnaire_id != questionnaire_id:
                abort(404)
        if not dimension.accessible_by(current_user()):
            abort(403)
        if not dimension.modifiable_by(current_user()):
            abort(403)
        if dimension.shadow:
            abort(403)

        question = dimension.new_question(data['text'])

        for k, v in data.items():
            if 'k' == 'template':
                if not current_has_minimum_role(Role.Contributor):
                    errors[k] = ['You need to be a contributor to publish '
                                 'templates.']
                    continue
            setattr(question, k, v)
        db.session.commit()

        data = QuestionSchema().dump(question).data
        response = {
            'message': 'Question created.',
            'question': data
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response, 201


class ShadowQuestionResource(Resource):
    @needs_minimum_role(Role.User)
    def post(self, questionnaire_id: int=None, dimension_id: int=None):
        schema = ShadowQuestionSchema()
        data, errors = schema.load(request.json)
        dimension = Dimension.query.get_or_404(dimension_id)
        question = Question.query.get_or_404(data['id'])

        if not dimension.accessible_by(current_user()):
            abort(403)
        if questionnaire_id is not None:
            if dimension.questionnaire_id != questionnaire_id:
                abort(404)
        if not dimension.modifiable_by(current_user()):
            abort(403)
        if dimension.shadow:
            abort(403)
        if question.shadow:
            abort(403)

        shadow_question = dimension.add_shadow_question(question)
        db.session.commit()

        data = QuestionSchema().dump(shadow_question).data
        return {
            'message': 'Question created.',
            'question': data
        }, 201


class QuestionListResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id: int=None, dimension_id: int=None):
        dimension = Dimension.query.get_or_404(dimension_id)
        if not dimension.accessible_by(current_user()):
            abort(403)
        if questionnaire_id is not None:
            if dimension.questionnaire_id != questionnaire_id:
                abort(404)

        schema = QuestionSchema(many=True)
        return schema.dump(dimension.questions).data


class TemplateQuestionListResource(Resource):
    def get(self):
        templates = Question.query.filter_by(_template=True).all()
        schema = QuestionSchema(many=True)
        return schema.dump(templates).data


api.add_resource(
    QuestionResource,
    '/api/question/<int:question_id>',
    '/api/dimension/<int:dimension_id>/question/<int:question_id>',
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>'
)

api.add_resource(
    ConcreteQuestionResource,
    '/api/dimension/<int:dimension_id>/concrete_question',
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/concrete_question'
)

api.add_resource(
    ShadowQuestionResource,
    '/api/dimension/<int:dimension_id>/shadow_question',
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/shadow_question'
)

api.add_resource(
    QuestionListResource,
    '/api/dimension/<int:dimension_id>/question',
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question'
)

api.add_resource(
    TemplateQuestionListResource,
    '/api/question/template'
)


ResourceBroker.add_resource_for(QuestionResource, Question, 'question_id')
