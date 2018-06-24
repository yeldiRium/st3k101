from flask import request
from flask_restful import Resource, abort

from api.v2 import api
from api.v2.schema.question import QuestionSchema
from auth.roles import needs_minimum_role, Role
from auth.users import current_user
from model.SQLAlchemy import db
from model.SQLAlchemy.models.Question import Question as Question, ConcreteQuestion

__author__ = "Noah Hummel"


class QuestionResource(Resource):

    @staticmethod
    def get_question_or_404(questionnaire_id=None, dimension_id=None,
                            question_id=None):
        if question_id is None:
            abort(404)

        question = Question.query.get_or_404(question_id)  # type: Question
        if dimension_id is not None:
            if question.dimension_id != dimension_id:
                abort(404)
        if questionnaire_id is not None:
            if question.dimension.questionnaire_id != questionnaire_id:
                abort(404)

        return question

    def get(self, **kwargs):
        question = self.get_question_or_404(**kwargs)

        if question.accessible_by(current_user()):
            schema = QuestionSchema()
            return schema.dump(question).data

        abort(404)

    @needs_minimum_role(Role.User)
    def patch(self, **kwargs):
        question = self.get_question_or_404(**kwargs)
        if not question.modifiable_by(current_user()):
            abort(404)

        schema = QuestionSchema()
        data, errors = schema.load(request.json, partial=True)
        for err in errors:
            del data[err]
        if not data:
            return {
                'message': 'Question not updated. Some errors occurred.',
                'errors': errors
            }, 400

        for k, v in data.keys:
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
        if not question.modifiable_by(current_user()):
            abort(404)
        data = QuestionSchema().dump(question).data
        db.session.delete(question)
        db.session.commit()
        return {
            'message': 'Question removed.',
            'question': data
        }


class ConcreteQuestionResource(Resource):

    def post(self, item_id=None):
        """
        Creates a new question
        :param item_id:
        :return:
        """
        if item_id is not None:
            abort(400, message='Can\'t specify item id on creation.')

        schema = QuestionSchema()

        data, errors = schema.load(request.json)
        if errors:
            return errors, 400

        question = ConcreteQuestion(text=data['text'])
        question.range = data['range']

        db.session.add(question)
        db.session.commit()
        return schema.dump(question).data

    def put(self, item_id):
        """
        Replaces question data with payload
        :param item_id:
        :return:
        """
        pass


class ShadowQuestionResource(Resource):
    pass


api.add_resource(
    QuestionResource,
    '/api/question/<int:question_id>',
    '/api/dimension/<int:dimension_id>/question/<int:question_id>',
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>'
)
