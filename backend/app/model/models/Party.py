from abc import abstractmethod
from typing import List

from model import db
from model.models.OwnershipBase import ownership_table
from auth.roles import Role


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

    @property
    @abstractmethod
    def roles(self) -> List[Role]:
        raise NotImplementedError
