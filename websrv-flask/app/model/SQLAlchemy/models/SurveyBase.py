from model.SQLAlchemy import db
from model.SQLAlchemy.v2_models.OwnershipBase import OwnershipBase


__author__ = "Noah Hummel"


class SurveyBase(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)

    # polymorphic config
    __tablename__ = 'survey_base'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    reference_id = db.Column(db.String(128))
