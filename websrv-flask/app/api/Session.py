from flask import request
from flask_restful import abort, Resource

from api import api
from api.schema.Session import LoginSchema, SessionSchema
from auth import users
from auth.roles import needs_role, Role
from framework.exceptions import UserNotLoggedInException, BadCredentialsException

__author__ = "Noah Hummel"


class SessionResource(Resource):

    def post(self):
        """
        Login route
        :return:
        """
        schema = LoginSchema()
        data, errors = schema.load(request.json)
        if errors:
            return errors, 400

        try:
            session_token = users.login(data['email'], data['password'])
            return SessionSchema().dump({'session_token': session_token}).data
        except BadCredentialsException:
            abort(404, message='User not found.')

    @needs_role(Role.User)
    def delete(self):
        """
        Logout route
        :return:
        """
        try:
            users.logout()
        except UserNotLoggedInException:
            # This should never happen
            abort(500, message='Hell froze over')
        return {'message': 'You were logged out.'}


api.add_resource(SessionResource, '/api/session', endpoint='session')
