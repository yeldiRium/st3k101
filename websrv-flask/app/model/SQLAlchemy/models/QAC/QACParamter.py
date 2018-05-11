from framework.internationalization import _, __
from model.SQLAlchemy import db

__author__ = "Noah Hummel"


class QACParameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_msgid = db.Column(db.String(120), nullable=False)
    description_msgid = db.Column(db.String(500), nullable=False)

    # polymorphism on, this is a base class
    type = db.Column(db.String(50))
    __tablename__ = 'qac_parameter'
    __mapper_args__ = {
        'polymorphic_identity': 'qac_parameter',
        'polymorphic_on': type
    }

    # foreign keys
    qac_module_id = db.Column(db.Integer, db.ForeignKey('qac_module.id'))

    def __init__(self, **kwargs):
        super(QACParameter, self).__init__(**kwargs)
        self.name = __("You forgot to assign a name to this QACParameter."
                       "Please assign a name to it! Please refer to the "
                       "documentation on QACParameter to learn how to do this.")
        self.description = __("You forgot to assign a description to this "
                              "QACParameter. Please assign a description to "
                              "it! Please refer to the documentation on "
                              "QACParameter to learn how to do this.")

    @property
    def name(self) -> str:
        return _(self.name_msgid)

    @name.setter
    def name(self, name_msgid: str):
        """
        Use __("The parameter name") from framework/internationalization to
        assign to this, otherwise it won't be included in the message catalogue.
        :param name_msgid: The name of the QACParameter.
        """
        self.name_msgid = name_msgid

    @property
    def description(self):
        return _(self.description_msgid)

    @description.setter
    def description(self, description_msgid: str):
        """
        Use __("The parameter description") from framework/internationalization
        to assign to this, otherwise it won't be included in the message
        catalogue.
        :param description_msgid: The description of the QACParameter.
        """
        self.description_msgid = description_msgid
