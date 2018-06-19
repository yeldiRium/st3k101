from flask import request
from flask_restful import abort, Resource

from api.v2 import api
from api.v2.schema.dataclient import DataClientSchema
from auth import users
from auth.roles import Role, needs_minimum_role, current_has_role, current_has_minimum_role
from auth.users import current_user
from framework.exceptions import UserExistsException
from model.SQLAlchemy import db
from model.SQLAlchemy.models.DataClient import DataClient

__author__ = "Noah Hummel"


class DataClientResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, item_id=None):
        schema = DataClientSchema()

        if item_id is not None and item_id != current_user().id:
            if not current_has_minimum_role(Role.Admin):
                abort(403, message='You are not allowed to access other user\'s'
                                   ' data.')
            dataclient = DataClient.query.get(item_id)
            if dataclient is None:
                abort(404)
            return schema.dump(dataclient).data

        else:
            return schema.dump(current_user()).data

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

    @needs_minimum_role(Role.User)
    def delete(self, item_id=None):
        if item_id is not None and item_id != current_user().id:
            if not current_has_minimum_role(Role.Admin):
                abort(403, message='You are not allowed to remove other user\'s'
                                   ' accounts.')
            dataclient = DataClient.query.get(item_id)
            if dataclient is None:
                abort(404)
            dataclient_data = DataClientSchema().dump(dataclient).data
            db.session.delete(dataclient)
            db.session.commit()
            return {
                'message': 'DataClient removed',
                'data_client': dataclient_data
            }

        else:
            dataclient_data = DataClientSchema().dump(current_user()).data
            db.session.delete(current_user())
            db.session.commit()
            return {
                'message': 'DataClient removed',
                'data_client': dataclient_data
            }

    @needs_minimum_role(Role.User)
    def put(self, item_id=None):
        if item_id is not None and item_id != current_user().id:
            if not current_has_minimum_role(Role.Admin):
                abort(403, message='You are not allowed to modify other user\'s'
                                   ' accounts.')
            dataclient = DataClient.query.get(item_id)
            if dataclient is None:
                abort(404)
        else:
            dataclient = current_user()

        schema = DataClientSchema(partial=True)
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]

        if 'roles' in data:
            if not current_has_minimum_role(Role.Admin):
                errors['roles'] = ['You are note allowed to change user\'s roles']
            dataclient.update_roles(data['roles'])
            del data['roles']
        for k, v in data.items():
            setattr(dataclient, k, v)
        db.session.commit()

        if data:
            response = {
                'message': 'DataClient updated.',
                'data_client': schema.dump(dataclient).data
            }
        else:
            response = {
                'message': 'DataClient not updated.'
            }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response


api.add_resource(DataClientResource, '/api/dataclient',
                 '/api/dataclient/<int:item_id>', endpoint='dataclient')
