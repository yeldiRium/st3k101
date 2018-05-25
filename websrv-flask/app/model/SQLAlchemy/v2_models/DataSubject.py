__author__ = "Noah Hummel"


from model.SQLAlchemy import db
from model.SQLAlchemy.v2_models.Person import Person


class DataSubject(Person):
    id = db.Column(db.Integer, db.ForeignKey(Person.id), primary_key=True)

    # polymorphic config
    __tablename__ = 'data_subject'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    email = db.Column(db.String(120), nullable=False)
    confirmation_token = db.Column(db.String(32))

    @staticmethod
    def get_or_create(email: str) -> "DataSubject":
        subject = DataSubject.query.filter_by(email=email).first()
        if subject is None:
            subject = DataSubject(email=email)
            db.session.add(subject)
        return subject
