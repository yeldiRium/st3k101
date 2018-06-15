from flask import request
from flask_restful import abort, Resource
from marshmallow import ValidationError

from api.v2 import api
from api.v2.schema.dataclient import DataClientSchema
from auth import users
from framework.exceptions import UserExistsException
from model.SQLAlchemy import db

__author__ = "Noah Hummel"


class DataClientResource(Resource):
    def get(self, item_id=None):
        if item_id is None:
            abort(400, message='You need to specify an id in order to use the'
                               'GET method.')

    def post(self, item_id=None):
        if item_id is not None:
            abort(400, message='Can\'t specify item id on creation.')

        schema = DataClientSchema()
        data, errors = schema.load(request.json)
        if errors:
            return errors, 400

        try:
            dataclient = users.register(data['email'], data['password'])
        except UserExistsException:
            return {'email': ['An user with that email address already exists.']}, 409

        del data['password']
        for k, v in data.items():
            setattr(dataclient, k, v)

        db.session.add(dataclient)
        db.session.commit()
        return schema.dump(dataclient).data

    def delete(self, item_id=None):
        if item_id is None:
            abort(400, message='You need to specify an id in order to use the'
                               'DELETE method.')


api.add_resource(DataClientResource, '/api/dataclient',
                 '/api/dataclient/<int:item_id>', endpoint='dataclient')
