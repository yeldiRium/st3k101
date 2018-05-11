from model.SQLAlchemy import db

from deprecated import deprecated

__author__ = "Noah Hummel"


class DataSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    confirmation_token = db.Column(db.String(32))

    question_results = db.relationship('QuestionResult', backref='data_subject',
                                       lazy=True, cascade='all, delete-orphan')

    @staticmethod
    def get_or_create(email: str) -> "DataSubject":
        subject = DataSubject.query.filter_by(email=email).first()
        if subject is None:
            subject = DataSubject(email=email)
            db.session.add(subject)
        return subject

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "email"')
    def email_hash(self) -> str:
        """
        Legacy shim for DataSubject.email_hash
        In version 2.0 emails will not be hashed, this shim is here
        for compatibility with code from version 1.0
        :return: The DataSubject's email address as hex hash
        """
        import hashlib
        email = self.email.encode("utf-8")
        hasher = hashlib.new('ripemd160')
        hasher.update(email)
        return hasher.hexdigest()
