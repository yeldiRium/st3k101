from flask import request
from flask_restful import abort, Resource

import auth.dataclient
import auth.session
from api import api
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
        schema = LtiRequestSchema()  # FIXME: implement this
        data, errors = schema.load(request.json)
        if errors:
            return errors, 400

        if not questionnaire.allow_embedded:
            abort(403)

        if questionnaire.lti_consumer_key != data['oauth_consumer_key']:
            abort(403, message='Invalid consumer key.')

        # use user_id as placeholder for email_address
        if 'lis_person_contact_email_primary' in data:
            email = data['lis_person_contact_email_primary']
        else:
            email = data['user_id']

        # get previously existing accounts for this DataSubject
        subject_by_mail = DataSubject.query.filter_by(email=email).first()
        subject_by_id = DataSubject.query.filter_by(lti_user_id=data['user_id']).first()

        # FIXME: choose right account and start session
        return {"sessionToken": "1337"}



api.add_resource(SessionResource, '/api/session', endpoint='session')
api.add_resource(LtiSessionResource, '/api/questionnaire/<int:questionnaire_id>/lti')
