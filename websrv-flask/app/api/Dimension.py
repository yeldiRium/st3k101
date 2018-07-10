from flask import request
from flask_restful import Resource, abort

from api import api
from framework.dependency_injection import ResourceBroker
from api.schema.Dimension import DimensionSchema, ShadowDimensionSchema
from auth.roles import current_has_minimum_role, Role, needs_minimum_role
from auth.users import current_user
from model import db
from model.models.Dimension import Dimension, ShadowDimension
from model.models.Questionnaire import Questionnaire

__author__ = "Noah Hummel"


class DimensionResource(Resource):
    def get(self, questionnaire_id=None, dimension_id=None):
        dimension = Dimension.query.get_or_404(dimension_id)
        if questionnaire_id is not None:
            if dimension.questionnaire_id != questionnaire_id:
                abort(404)
        if not dimension.accessible_by(current_user()):
            abort(404)
        return DimensionSchema().dump(dimension).data

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
                                 'responsible for the Dimension\'s content.'.format(k)]
                    continue
            else:
                if k == 'template' and not current_has_minimum_role(Role.Contributor):
                    errors[k] = ['You need to be a contributor to publish templates.']
                    continue
            setattr(dimension, k, v)
        db.session.commit()

        response = {
            'message': 'Dimension updated.',
            'dimension': schema.dump(dimension).data
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
        data = DimensionSchema().dump(dimension).data
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

        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        if not questionnaire.modifiable_by(current_user()):
            abort(403)
        if questionnaire.shadow:
            abort(403)

        dimension = questionnaire.new_dimension(data['name'])
        for k, v in data.items():
            if k == 'template':
                if not current_has_minimum_role(Role.Contributor):
                    errors[k] = ['You need to be a contributor to publish '
                                 'templates.']
                    continue
            setattr(dimension, k, v)
        db.session.commit()

        data = DimensionSchema().dump(dimension).data
        response = {
            'message': 'Dimension created.',
            'dimension': data
        }
        if errors:
            response['message'] += ' Some errors occurred.'
            response['errors'] = errors
        return response, 201


class ShadowDimensionResource(Resource):
    @needs_minimum_role(Role.User)
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

        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        dimension = Dimension.query.get_or_404(data['id'])
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        if not questionnaire.modifiable_by(current_user()):
            abort(403)
        if questionnaire.shadow:
            abort(403)
        if dimension.shadow:
            abort(403)

        shadow_dimension = questionnaire.add_shadow_dimension(dimension)
        db.session.commit()

        data = DimensionSchema().dump(shadow_dimension).data
        return {
            'message': 'Dimension created.',
            'dimension': data
        }


class DimensionListResource(Resource):
    @needs_minimum_role(Role.User)
    def get(self, questionnaire_id=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(404)
        schema = DimensionSchema(many=True)
        return schema.dump(questionnaire.dimensions).data


class TemplateDimensionListResource(Resource):
    def get(self):
        templates = Dimension.query.filter_by(_template=True).all()
        schema = DimensionSchema(many=True)
        return schema.dump(templates).data


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
