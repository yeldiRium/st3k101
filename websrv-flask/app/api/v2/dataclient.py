from flask import request
from flask_restful import abort, Resource

from api.v2 import api
from api.v2.dependency_injection import ResourceBroker
from api.v2.schema.dataclient import DataClientSchema
from auth import users
from auth.roles import Role, needs_minimum_role, current_has_minimum_role
from auth.users import current_user
from framework.exceptions import UserExistsException
from model.SQLAlchemy import db
from model.SQLAlchemy.models.DataClient import DataClient

__author__ = "Noah Hummel"


class CurrentDataClientResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self):
        return DataClientSchema().dump(current_user())

    def post(self):
        schema = DataClientSchema()
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'DataClient not created. Some errors occurred.',
                'errors': errors
            }, 400

        try:
            dataclient = users.register(data['email'], data['password'])
        except UserExistsException:
            return {
                'message': 'DataClient not created. Some errors occurred.',
                'errors': {
                    'email': ['An user with that email address already exists.']
                }
            }, 409

        del data['password']
        for k, v in data.items():
            setattr(dataclient, k, v)

        db.session.add(dataclient)
        db.session.commit()
        return schema.dump(dataclient), 201

    @needs_minimum_role(Role.User)
    def patch(self):
        dataclient = current_user()
        schema = DataClientSchema(partial=True)
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]

        if not data:
            return {
                'message': 'DataClient not updated. Some errors occurred',
                'errors': errors
            }, 400

        for k, v in data.items():
            if k == 'roles':
                if not current_has_minimum_role(Role.Admin):
                    errors[k] = ['You are note allowed to change user\'s '
                                 'roles']
                    continue
                dataclient.update_roles(data['roles'])
            setattr(dataclient, k, v)
        db.session.commit()

        response = {
            'message': 'DataClient updated.',
            'data_client': schema.dump(dataclient)
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response

    @needs_minimum_role(Role.User)
    def delete(self):
        dataclient_data = DataClientSchema().dump(current_user())
        db.session.delete(current_user())
        db.session.commit()
        users.logout()
        return {
            'message': 'DataClient removed',
            'data_client': dataclient_data
        }


class DataClientResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, dataclient_id=None):
        schema = DataClientSchema()

        if dataclient_id != current_user().id:
            if not current_has_minimum_role(Role.Admin):
                abort(403, message='You are not allowed to access other user\'s'
                                   ' data.')
        dataclient = DataClient.query.get_or_404(dataclient_id)
        return schema.dump(dataclient)

    @needs_minimum_role(Role.User)
    def delete(self, dataclient_id=None):
        if dataclient_id != current_user().id:
            if not current_has_minimum_role(Role.Admin):
                abort(403, message='You are not allowed to remove other user\'s'
                                   ' accounts.')
        dataclient = DataClient.query.get_or_404(dataclient_id)
        dataclient_data = DataClientSchema().dump(dataclient)
        db.session.delete(dataclient)
        db.session.commit()
        return {
            'message': 'DataClient removed',
            'data_client': dataclient_data
        }

    @needs_minimum_role(Role.User)
    def patch(self, dataclient_id=None):
        if dataclient_id != current_user().id:
            if not current_has_minimum_role(Role.Admin):
                abort(403, message='You are not allowed to modify other user\'s'
                                   ' accounts.')
        dataclient = DataClient.query.get_or_404(dataclient_id)

        schema = DataClientSchema(partial=True)
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]

        if not data:
            return {
                'message': 'DataClient not updated. Some errors occurred',
                'errors': errors
            }, 400

        for k, v in data.items():
            if k == 'roles':
                if not current_has_minimum_role(Role.Admin):
                    errors[k] = ['You are note allowed to change user\'s '
                                 'roles']
                    continue
                dataclient.update_roles(data['roles'])
            setattr(dataclient, k, v)
        db.session.commit()

        response = {
            'message': 'DataClient updated.',
            'data_client': schema.dump(dataclient)
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response


class DataClientVerificationResource(Resource):
    def get(self, token: str=None):
        dataclient = DataClient.query.filter_by(verification_token=token).first()
        if dataclient is None:
            abort(404)
        dataclient.verified = True
        dataclient.verification_token = None
        db.session.commit()
        return  # TODO redirect


api.add_resource(DataClientResource, '/api/dataclient/<int:dataclient_id>')
api.add_resource(CurrentDataClientResource, '/api/dataclient')
api.add_resource(DataClientVerificationResource,
                 '/api/dataclient/verify/<token>')

ResourceBroker.add_resource_for(DataClientResource, DataClient, 'dataclient_id')
