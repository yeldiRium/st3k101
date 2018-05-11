from datetime import datetime

from deprecated import deprecated
from flask import g

from framework.exceptions import QuestionnaireNotFoundException, ObjectDoesntExistException
from framework.internationalization import _
from framework.internationalization.babel_languages import BabelLanguage
from model.SQLAlchemy import db, translation_hybrid, MUTABLE_HSTORE
from model.SQLAlchemy.models.DataClient import DataClient
from model.SQLAlchemy.models.QAC.QACModules import QAC
from model.SQLAlchemy.models.Question import Question
from model.SQLAlchemy.models.QuestionGroup import QuestionGroup
from model.SQLAlchemy.models.Questionnaire import Questionnaire

__author__ = "Noah Hummel"


class Survey(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    # translatable columns
    name_translations = db.Column(MUTABLE_HSTORE)
    name = translation_hybrid(name_translations)

    # relationships
    questionnaires = db.relationship('Questionnaire', backref='survey',
                                     cascade='all, delete-orphan')

    # foreign keys
    data_client_id = db.Column(db.Integer, db.ForeignKey('data_client.id'))

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "original_language"')
    def original_locale(self) -> str:
        return self.original_language.name

    def __init__(self, **kwargs):
        super(Survey, self).__init__(**kwargs)
        self.date_created = datetime.today()
        self.original_language = g._language  # TODO: set before request

    @staticmethod
    @deprecated(version='2.0', reason='Use Survey() constructor directly')
    def create_survey(name: str) -> "Survey":
        return Survey(name=name)

    @deprecated(version='2.0', reason='Use Survey.name directly')
    def set_name(self, name: str) -> None:
        self.name = name

    @deprecated(version='2.0', reason='Use Questionnaire() constructor directly and pass survey, '
                                      'or use Survey.questionnaires.append().')
    def add_new_questionnaire(self, name: str, description: str) \
            -> Questionnaire:
        return Questionnaire(name=name, description=description, survey=self)

    def add_new_questionnaire_from_template(self, name: str, description: str,
                                            template_id: str) -> Questionnaire:
        """
        Creates a new Questionnaire for the Survey, either using one of the
        template files provided, or copying the contents of another.
        :param name: The name of the new Questionnaire.
        :param description: The description of the new Questionnaire.
        :param template_id: The uuid of the Questionnaire that is used as
                         a template, or the name of a Questionnaire
                         specified in a template file.
        :return: The newly created Questionnaire instance.
        """
        # first look in local template path
        template_files = Questionnaire.get_available_templates()

        if template_id in template_files:
            template_path = template_files[template_id]
            questionnaire = Questionnaire.from_yaml(template_path)
            self.questionnaires.append(questionnaire)
            return questionnaire

        # if template is not found on disk try getting by uuid
        template = Questionnaire.query.get(template_id)
        if template is None:
            raise ObjectDoesntExistException

        # if template is in a different language, indicate that foreign
        # language was copied
        foreign_template = template.original_language != g._language
        template_language = template.original_language
        if foreign_template:
            name = _("From template: ") + name + " ({})".format(template_language)
            description = _("From template: ") + description + " ({})".format(
                template_language)

        questionnaire = Questionnaire(name=name, description=description,
                                      survey=self)

        for template_qg in template.question_groups:

            group_name = template_qg.name
            if foreign_template:
                # Don't just copy name over, prepend notice that it's copied
                # from a different language
                group_name = _("From template: ") + group_name + "({})".format(
                    template_language)

            new_group = QuestionGroup(name=group_name,
                                      questionnaire=questionnaire,
                                      color=template_qg.color,
                                      text_color=template_qg.text_color)

            for template_q in template_qg.questions:
                question_text = template_q.text
                if foreign_template:
                    question_text = _("From template: ") + template_q.text + \
                                    "({})".format(template_language)

                Question(text=question_text, question_group=new_group)

        for qac_module in template.qac_modules:
            new_qac_module = QAC[qac_module.qac_id]()
            questionnaire.add_qac_module(new_qac_module)

        return questionnaire

    @deprecated(version='2.0', reason='Is implemented by database cascades.'
                                      'Use Survey.questionnaires.remove(questionnaire) instead.')
    def remove_questionnaire(self, questionnaire: Questionnaire):
        """
        Removes a Questionnaire from the Survey and the database.
        :param questionnaire: The Questionnaire to remove.
        """
        try:
            self.questionnaires.remove(questionnaire)
        except KeyError as _:
            raise QuestionnaireNotFoundException(self.name, questionnaire.name)

    @property
    def owner(self) -> DataClient:
        return self.data_client
