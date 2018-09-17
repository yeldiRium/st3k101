from flask import request
from flask_restful import abort, Resource

import auth.dataclient
import auth.datasubject
import auth.session
from api import api
from api.schema.LtiRequestSchema import LtiRequestSchema
from api.schema.Session import LoginSchema, SessionSchema
from auth.roles import needs_role, Role
from framework.exceptions import UserNotLoggedInException, BadCredentialsException
from model.models.DataSubject import DataSubject
from model.models.Questionnaire import Questionnaire

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
            session_token = auth.dataclient.login(data['email'], data['password'])
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
            auth.session.logout()
        except UserNotLoggedInException:
            # This should never happen
            abort(500, message='Hell froze over')
        return {'message': 'You were logged out.'}


class LtiSessionResource(Resource):
    def post(self, questionnaire_id: int=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        schema = LtiRequestSchema()
        data, errors = schema.load(request.json)
        if errors:
            return errors, 400

        if not questionnaire.allow_embedded:
            abort(403)

        if questionnaire.lti_consumer_key != data['oauth_consumer_key']:
            abort(403, message='Invalid consumer key.')

        subject = DataSubject.get_or_create(lti_user_id=data['user_id'])
        if 'lis_person_contact_email_primary' in data:
            subject.email = data['lis_person_contact_email_primary']

        session_token = auth.datasubject.new_lti_session(subject.lti_user_id)

        if session_token is not None:
            return {"sessionToken": session_token}


api.add_resource(SessionResource, '/api/session', endpoint='session')
api.add_resource(LtiSessionResource, '/api/questionnaire/<int:questionnaire_id>/lti')
