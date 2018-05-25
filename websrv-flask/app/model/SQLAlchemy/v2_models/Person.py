from model.SQLAlchemy import db
from model.SQLAlchemy.v2_models.OwnershipBase import ownership_table


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # polymorphic config
    type = db.Column(db.String(50))
    __tablename__ = 'person'
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type
    }

    owned_objects = db.relationship('OwnershipBase', back_populates='owners',
                                    secondary=ownership_table)
