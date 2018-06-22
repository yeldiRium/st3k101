from flask import request
from flask_restful import Resource, abort

from api.v2 import api
from api.v2.schema.questionnaire import QuestionnaireSchema, ShadowQuestionnaireSchema
from auth.roles import needs_minimum_role, Role, current_has_minimum_role
from auth.users import current_user
from model.SQLAlchemy import db
from model.SQLAlchemy.models.DataClient import DataClient
from model.SQLAlchemy.models.OwnershipBase import query_owned
from model.SQLAlchemy.models.Questionnaire import Questionnaire, ConcreteQuestionnaire, ShadowQuestionnaire

__author__ = "Noah Hummel"


class QuestionnaireResource(Resource):
    @staticmethod
    def dump(schema, questionnaire):
        data = {
            **schema.dump(questionnaire).data,
            'href': api.url_for(
                QuestionnaireResource,
                questionnaire_id=questionnaire.id
            )
        }
        if data['shadow']:
            data['shadow_href'] = api.url_for(
                QuestionnaireResource,
                questionnaire_id=questionnaire.concrete_id
            )
        return data

    def get(self, questionnaire_id=None):
        schema = QuestionnaireSchema()
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        return self.dump(schema, questionnaire)

    @needs_minimum_role(Role.User)
    def patch(self, questionnaire_id=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.modifiable_by(current_user()):
            abort(404)

        schema = QuestionnaireSchema(partial=True)
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'Questionnaire not updated. Some errors occurred.',
                'errors': errors
            }, 400

        shadow_attributes = ['published', 'allow_embedded', 'xapi_target']
        for k, v in data.items():
            if isinstance(questionnaire, ShadowQuestionnaire):
                if k not in shadow_attributes:
                    errors[k] = ['Can\'t update {} of a ShadowQuestionnaire. The '
                                 'contributor owning the template is responsible '
                                 'for the Questionnaire\'s content.'.format(k)]
                    continue
            else:
                if k == 'template' and not current_has_minimum_role(Role.Contributor):
                    errors[k] = ['You need to be a contributor to publish templates.']
                    continue
            setattr(questionnaire, k, v)
        db.session.commit()

        response = {
            'message': 'Questionnaire updated.',
            'questionnaire': self.dump(schema, questionnaire)
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response

    @needs_minimum_role(Role.User)
    def delete(self, questionnaire_id=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.modifiable_by(current_user()):
            abort(404)
        data = self.dump(QuestionnaireSchema(), questionnaire)
        questionnaire.delete()
        db.session.commit()
        return {
            'message': 'Questionnaire removed.',
            'questionnaire': data
        }


class QuestionnaireListResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, dataclient_id=None):
        if dataclient_id is None:
            dataclient = current_user()
        else:
            if not current_has_minimum_role(Role.Admin):
                abort(403)
            dataclient = DataClient.query.get(dataclient_id)

        query = query_owned(DataClient, dataclient.id, Questionnaire)
        questionnaires = query.all()

        schema = QuestionnaireSchema()
        return [QuestionnaireResource.dump(schema, q) for q in questionnaires]


class TemplateQuestionnaireListResource(Resource):
    def get(self):
        templates = Questionnaire.query.filter_by(_template=True).all()
        schema = QuestionnaireSchema()
        return [QuestionnaireResource.dump(schema, q) for q in templates]


class ConcreteQuestionnaireResource(Resource):
    @needs_minimum_role(Role.User)
    def post(self):
        schema = QuestionnaireSchema()
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'Questionnaire not created. Some errors occurred.',
                'errors': errors
            }, 400

        questionnaire = ConcreteQuestionnaire(data['name'], data['description'])
        for k, v in data.items():
            if k == 'template' and not current_has_minimum_role(Role.Contributor):
                errors[k] = 'You need to be a contributor to publish templates.'
                continue
        db.session.add(questionnaire)
        db.session.commit()

        response = {
            'message': 'Questionnaire created.',
            'questionnaire': QuestionnaireResource.dump(schema, questionnaire)
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response, 201


class ShadowQuestionnaireResource(Resource):
    def post(self):
        schema = ShadowQuestionnaireSchema()
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]

        if not data:
            return {
                'message': 'Questionnaire not created. Some errors occurred.',
                'errors': errors
            }, 400

        concrete_questionnaire = ConcreteQuestionnaire.query.get_or_404(data['id'])
        shadow_questionnaire = ShadowQuestionnaire(concrete_questionnaire)
        db.session.add(shadow_questionnaire)
        db.session.commit()
        return QuestionnaireResource.dump(QuestionnaireSchema(), shadow_questionnaire), 201


api.add_resource(
    QuestionnaireResource,
    '/api/questionnaire/<int:questionnaire_id>',
    endpoint='questionnaire'
)

api.add_resource(
    ConcreteQuestionnaireResource,
    '/api/dataclient/concrete_questionnaire'
)

api.add_resource(
    ShadowQuestionnaireResource,
    '/api/dataclient/shadow_questionnaire'
)

api.add_resource(
    QuestionnaireListResource,
    '/api/dataclient/questionnaire',
    '/api/dataclient/<int:dataclient_id>/questionnaire',
)

api.add_resource(
    TemplateQuestionnaireListResource,
    '/api/questionnaire/template'
)