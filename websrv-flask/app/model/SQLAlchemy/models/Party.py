from model.SQLAlchemy import db
from model.SQLAlchemy.models.OwnershipBase import ownership_table


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # polymorphic config
    person_type = db.Column(db.String(50))
    __tablename__ = 'person'
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': person_type
    }

    owned_objects = db.relationship('OwnershipBase', back_populates='owners',
                                    secondary=ownership_table)
