from flask import request
from flask_restful import Resource, abort

from api.v2 import api
from api.v2.dependency_injection import ResourceBroker
from api.v2.questionnaire import QuestionnaireResource
from api.v2.schema.dimension import DimensionSchema, ShadowDimensionSchema
from api.v2.schema.questionnaire import QuestionnaireSchema
from app import app
from auth.roles import current_has_minimum_role, Role, needs_minimum_role
from auth.users import current_user
from model.SQLAlchemy import db
from model.SQLAlchemy.models.Dimension import Dimension, ShadowDimension, ConcreteDimension
from model.SQLAlchemy.models.Questionnaire import Questionnaire, ConcreteQuestionnaire

__author__ = "Noah Hummel"


class DimensionResource(Resource):
    def get(self, questionnaire_id=None, dimension_id=None):
        dimension = Dimension.query.get_or_404(dimension_id)
        if questionnaire_id is not None:
            if dimension.questionnaire_id != questionnaire_id:
                abort(404)
        if not dimension.accessible_by(current_user()):
            abort(404)
        return DimensionSchema().dump(dimension)

    @needs_minimum_role(Role.User)
    def patch(self, questionnaire_id=None, dimension_id=None):
        dimension = Dimension.query.get_or_404(dimension_id)
        if questionnaire_id is not None:
            if dimension.questionnaire_id != questionnaire_id:
                abort(404)
        if not dimension.accessible_by(current_user()):
            abort(404)
        if not dimension.modifiable_by(current_user()):
            abort(403)

        schema = DimensionSchema(partial=True)
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'Dimension not updated. Some errors occurred.',
                'errors': errors
            }, 400

        shadow_attributes = ['randomize_question_order']
        for k, v in data.items():
            if isinstance(dimension, ShadowDimension):
                if k not in shadow_attributes:
                    errors[k] = ['Can\'t update {} of a ShadowDimension. The '
                                 'contributor owning the template is '
                                 'responsible for the Dimension\'s content.']
                    continue
            else:
                if k == 'template' and not current_has_minimum_role(Role.Contributor):
                    errors[k] = ['You need to be a contributor to publish templates.']
                    continue
            setattr(dimension, k, v)
        db.session.commit()

        response = {
            'message': 'Dimension updated.',
            'dimension': schema.dump(dimension)
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response

    @needs_minimum_role(Role.User)
    def delete(self, questionnaire_id=None, dimension_id=None):
        dimension = Dimension.query.get_or_404(dimension_id)
        if questionnaire_id is not None:
            questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        else:
            questionnaire = dimension.questionnaire
        if not dimension.accessible_by(current_user()):
            abort(404)
        if not dimension.modifiable_by(current_user()):
            abort(403)
        data = DimensionSchema().dump(dimension)
        questionnaire.remove_dimension(dimension)
        db.session.commit()
        return {
            'message': 'Dimension removed.',
            'dimension': data
        }


class ConcreteDimensionResource(Resource):
    @needs_minimum_role(Role.User)
    def post(self, questionnaire_id=None):
        schema = DimensionSchema()
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]
        if not data:
            return {
                'message': 'Dimension not created. Some errors occurred.',
                'errors': errors
            }, 400

        questionnaire = ConcreteQuestionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        if not questionnaire.modifiable_by(current_user()):
            abort(403)
        questionnaire.new_dimension(data['name'])
        for k, v in data.items():
            if k == 'template' and not current_has_minimum_role(Role.Contributor):
                errors[k] = 'You need to be a contributor to publish templates.'
                continue
        db.session.commit()

        data = QuestionnaireSchema().dump(questionnaire)
        response = {
            'message': 'Dimension created.',
            'questionnaire': data
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response, 201


class ShadowDimensionResource(Resource):
    def post(self, questionnaire_id=None):
        schema = ShadowDimensionSchema()
        data, errors = schema.load(request.json)
        for err in errors:
            if err in data:
                del data[err]

        if not data:
            return {
                'message': 'Dimension not created. Some errors occurred.',
                'errors': errors
            }, 400

        questionnaire = ConcreteQuestionnaire.query.get_or_404(questionnaire_id)
        concrete_dimension = ConcreteDimension.query.get_or_404(data['id'])
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        if not questionnaire.modifiable_by(current_user()):
            abort(403)
        questionnaire.add_shadow_dimension(concrete_dimension)
        db.session.commit()

        data = QuestionnaireSchema().dump(questionnaire)
        return {
            'message': 'Dimension created.',
            'questionnaire': data
        }


class DimensionListResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        schema = DimensionSchema(many=True)
        return schema.dump(questionnaire.dimensions)


class TemplateDimensionListResource(Resource):
    def get(self):
        templates = Dimension.query.filter_by(_template=True).all()
        schema = DimensionSchema(many=True)
        return schema.dump(templates)


api.add_resource(
    DimensionResource,
    '/api/dimension/<int:dimension_id>',
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>'
)

api.add_resource(
    ConcreteDimensionResource,
    '/api/questionnaire/<int:questionnaire_id>/concrete_dimension'
)

api.add_resource(
    ShadowDimensionResource,
    '/api/questionnaire/<int:questionnaire_id>/shadow_dimension'
)

api.add_resource(
    DimensionListResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension'
)

api.add_resource(
    TemplateDimensionListResource,
    '/api/dimension/template'
)

ResourceBroker.add_resource_for(DimensionResource, Dimension, 'dimension_id')
