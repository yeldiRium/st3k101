__author__ = "Noah Hummel"


from model.SQLAlchemy import db


ownership_table = db.Table('ownership_assoc', db.Model.metadata,
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('ownership_base_id', db.Integer, db.ForeignKey('ownership_base.id'))
)


class OwnershipBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # polymorphic config
    type = db.Column(db.String(50))
    __tablename__ = 'ownership_base'
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type
    }

    owners = db.relationship('Person', back_populates='owned_objects',
                             secondary=ownership_table)
