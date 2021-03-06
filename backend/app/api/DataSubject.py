from flask import request
from flask_restful import Resource
from sqlalchemy import or_

from api import api
from api.schema.DataSubject import DataSubjectQuerySchema, DataSubjectSchema
from auth.roles import Role, needs_minimum_role
from model import db
from model.models.DataSubject import DataSubject

__author__ = "Noah Hummel"


class DataSubjectListResource(Resource):
    @needs_minimum_role(Role.Admin)
    def post(self):
        data, errors = DataSubjectQuerySchema().load(request.json, partial=True)
        if errors:
            return {
                'message': 'Your query contained errors.',
                'errors': errors
            }, 400

        query = DataSubject.query
        predicates = []
        if 'email' in data:
            predicates.append(DataSubject.email.like(data['email']))
        if 'moodle_username' in data:
            predicates.append(DataSubject.moodle_username.like(data['moodle_username']))
        if 'source' in data:
            predicates.append(DataSubject.source.like(data['source']))
        if predicates:
            query = query.filter(or_(*predicates))

        data_subjects = query.all()
        return DataSubjectSchema(many=True).dump(data_subjects)


class DataSubjectResource(Resource):
    @needs_minimum_role(Role.Admin)
    def delete(self, datasubject_id):
        data_subject = DataSubject.query.get_or_404(datasubject_id)
        for obj in data_subject.owned_objects:
            db.session.delete(obj)
        db.session.delete(data_subject)
        db.session.commit()
        return {
            'message': 'DataSubject and all personal data deleted.'
        }


api.add_resource(
    DataSubjectListResource,
    '/api/datasubject'
)

api.add_resource(
    DataSubjectResource,
    '/api/datasubject/<int:datasubject_id>'
)
