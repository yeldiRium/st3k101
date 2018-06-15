from flask import request
from flask_restful import Resource, abort

from api.v2 import api
from api.v2.schema.question import QuestionSchema
from auth.users import current_user
from model.SQLAlchemy import db
from model.SQLAlchemy.models.Question import Question as Question, ConcreteQuestion

__author__ = "Noah Hummel"


class QuestionResource(Resource):
    def get(self, item_id=None):
        """
        Returns the question
        :param item_id:
        :return:
        """
        if item_id is None:
            abort(404)

        schema = QuestionSchema()
        schema.context = {'resource': QuestionResource}

        question = Question.query.get(item_id)
        if question is None:
            abort(404)

        if current_user() in question.owners or question.public:
            return schema.dump(question).data

        abort(404)

    def post(self, item_id=None):
        """
        Creates a new question
        :param item_id:
        :return:
        """
        if item_id is not None:
            abort(400, message='Can\'t specify item id on creation.')

        schema = QuestionSchema()
        schema.context = {'resource': QuestionResource}

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


api.add_resource(QuestionResource, '/api/question/<int:item_id>',
                 '/api/question', endpoint='question')
