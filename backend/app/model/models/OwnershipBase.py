from auth.roles import Role

__author__ = "Noah Hummel"


from model import db


ownership_table = db.Table('ownership_assoc', db.Model.metadata,
    db.Column('person_id', db.Integer, db.ForeignKey('person.id', ondelete='CASCADE', onupdate='CASCADE')),
    db.Column('ownership_base_id', db.Integer, db.ForeignKey('ownership_base.id', ondelete='CASCADE', onupdate='CASCADE'))
)


def query_owned(person_type: db.Model, person_id: int, owned_type: db.Model):
    query = owned_type.query.join(ownership_table).join(person_type).\
            filter((ownership_table.c.person_id == person_type.id) &
                   (ownership_table.c.ownership_base_id == owned_type.id)).\
            filter(person_type.id == person_id)
    return query


class OwnershipBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # polymorphic config
    ownership_base_type = db.Column(db.String(50))
    __tablename__ = 'ownership_base'
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': ownership_base_type
    }

    owners = db.relationship('Party', back_populates='owned_objects',
                             secondary=ownership_table)

    def accessible_by(self, party):
        if party is None:
            return False
        if Role.Root in party.roles:
            return True
        if Role.Admin in party.roles:
            return True
        return party in self.owners
