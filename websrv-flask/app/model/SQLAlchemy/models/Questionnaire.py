import os
from typing import Sized, List, Optional, Dict, Any

import yaml
from deprecated import deprecated
from flask import g

from framework.exceptions import QuestionGroupNotFoundException, QACNotEnabledException, YAMLTemplateInvalidException, \
    QACAlreadyEnabledException
from framework.internationalization import _
from framework.internationalization.babel_languages import BabelLanguage
from model.SQLAlchemy import db, translation_hybrid, HSTORE
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from model.SQLAlchemy.models.QAC.QACModules.EMailVerificationQAC import EMailVerificationQAC
from model.SQLAlchemy.models.QAC.QACModules.TOSQAC import TOSQAC
from model.SQLAlchemy.models.Question import Question
from model.SQLAlchemy.models.QuestionGroup import QuestionGroup
from model.SQLAlchemy.models.QuestionResult import QuestionResult

__author__ = "Noah Hummel"


class Questionnaire(db.Model):
    """
    A Questionnaire is a collection of Questions which are grouped into
    QuestionGroups. A Questionnaire is targeted to a specific audience.
    It can have a number of Questionnaire Access Control Modules (QACModules)
    enabled on it.
    A Questionnaire is contained in a survey.
    """
    # columns
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False)

    # translatable columns
    name_translations = db.Column(HSTORE)
    name = translation_hybrid(name_translations)
    description_translations = db.Column(HSTORE)
    description = translation_hybrid(description_translations)

    # relationships
    question_groups = db.relationship('QuestionGroup', backref='questionnaire',
                                      cascade='all, delete-orphan')
    qac_modules = db.relationship('QACModule')

    # foreign keys
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "original_language", new type: BabelLanguage')
    def original_locale(self) -> str:
        return self.original_language.name

    @original_locale.setter
    @deprecated(version='2.0', reason='Attribute has been renamed to "original_language", new type: BabelLanguage')
    def original_locale(self, language_id: str):
        lang = BabelLanguage[language_id]
        self.original_language = lang

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "question_groups"')
    def questiongroups(self) -> Sized[QuestionGroup]:
        return self.question_groups

    @property
    def question_count(self) -> int:
        """
        :return: The number of questions associated with the Questionnaire.
        """
        count = 0
        for qg in self.question_groups:
            count += len(qg.questions)
        return count

    @property
    def answer_count(self) -> int:
        """
        :return: The number of verified answers for the Questionnaire.
        """
        count = 0
        for qg in self.question_groups:
            for q in qg.questions:
                verified_results = QuestionResult.query.filter_by(question=q,
                                                                  verified=True)
                count += len(verified_results)
        return count

    def __init__(self, name: str, description: str, **kwargs):
        super(Questionnaire, self).__init__(name=name, description=description,
                                            **kwargs)
        self.qac_modules = [TOSQAC(), EMailVerificationQAC()]
        self.original_language = BabelLanguage[g._language]  # FIXME: set g._language before request

    @staticmethod
    @deprecated(version='2.0', reason='Use Questionnaire() constructor directly')
    def create_questionnaire(name: str, description: str) -> 'Questionnaire':
        """
        Factory method for creating a new Questionnaire with default values.
        :param name: The name of the new Questionnaire.
        :param description: The description text of the new Questionnaire.
        :return: The newly created Questionnaire instance.
        """
        return Questionnaire(name=name, description=description)

    @deprecated(version='2.0', reason='Use Questionnaire.name directly')
    def set_name(self, name: str):
        self.name = name

    @deprecated(version='2.0', reason='Use Questionnaire.description directly')
    def set_description(self, description: str):
        self.description = description

    @deprecated(version='2.0', reason='Use QuestionGroup() constructor directly and pass questionnaire')
    def add_question_group(self, name: str) -> QuestionGroup:
        """
        Creates a new QuestionGroup and adds it to the Questionnaire.
        :param name: The name of the new QuestionGroup.
        :return: The newly created QuestionGroup instance.
        """
        return QuestionGroup(name=name, questionnaire=self)

    @deprecated(version='2.0', reason='Will be implemented by db triggers in the future')
    def remove_question_group(self, question_group: QuestionGroup):
        """
        Removes a QuestionGroup from the Questionnaire and the database.
        :param question_group: The QuestionGroup to remove.
        """
        self.question_groups.remove(question_group)
        db.session.delete(question_group)

    @deprecated(version='2.0', reason='Use Question() constructor directly and pass question_group')
    def add_question_to_group(self, question_group: QuestionGroup,
                              text: str) -> Question:
        if question_group not in self.question_groups:
            raise QuestionGroupNotFoundException
        return Question(text=text, question_group=question_group)

    @deprecated(version='2.0', reason='Will be implemented by db triggers in the future')
    def remove_question_from_group(self, question_group: QuestionGroup,
                                   question: Question) -> QuestionGroup:
        """
        Removes a Question from the given QuestionGroup.
        The QuestionGroup has to belong to the Questionnaire.
        :param question_group: The QuestionGroup to remove from.
        :param question: The Question to remove.
        :return: The QuestionGroup that was removed from.
        """
        if question_group not in self.question_groups:
            raise QuestionGroupNotFoundException
        self.question_groups.remove(question)
        db.session.delete(question)
        return question_group

    @deprecated(version='2.0', reason='Use Questionnaire.qac_modules directly')
    def get_qac_modules(self) -> List[QACModule]:
        return self.qac_modules

    def add_qac_module(self, qac_module: QACModule):
        if qac_module in self.qac_modules:
            raise QACAlreadyEnabledException
        self.qac_modules.append(qac_module)

    def get_qac_module_by_qac_id(self, qac_id: str) -> Optional[QACModule]:
        """
        Returns QACModule with given qac_id (previously name.msgid)
        if it is present in Questionnaire.qac_modules
        :param qac_id:
        :return: The QACModule or None if not present
        """
        qac_module = None
        for qm in self.qac_modules:
            if qm.qac_id == qac_id:
                qac_module = qm
                break
        return qac_module

    @deprecated(version='2.0', reason='QACModule.name is deprecated, use QACModule.qac_id instead.')
    def get_qac_module(self, name: str) -> Optional[QACModule]:
        return self.get_qac_module_by_qac_id(name)

    @deprecated(version='2.0', reason='Will be implemented by db triggers in the future. '
                                      'Use Questionnaire.get_qac_module_by_qac_id to acquire qac and remove directly.')
    def remove_qac_module(self, qac_id: str):
        """
        Removes a QACModule from this Questionnaire and the database.
        Raises QACNotEnabledException if QACModule is not present
        in the Questionnaire.
        :param qac_id: The qac_id (previously name.msgid) of
                       the QACModule
        """
        qac_module = self.get_qac_module_by_qac_id(qac_id)
        if qac_module is None:
            raise QACNotEnabledException
        self.qac_modules.remove(qac_module)
        db.session.delete(qac_module)  # TODO: implement as cascade

    @staticmethod
    def parse_yaml(path_to_yaml: str) -> Dict[str, Any]:
        """
        Parses a YAMl template file for Questionnaire and raises Exceptions if
        the schema is invalid.
        :param path_to_yaml: str Path to the file to parse
        :return: dict The parsed YAML file.
        """
        with open(path_to_yaml) as fd:
            contents = yaml.load(fd)
        schema = {
            "name": str,
            "description": str,
            "questions": dict
        }
        try:
            if type(contents) != type(schema):
                raise Exception(_("Template needs to be a dictionary"))
            for k, v in schema.items():
                if k not in contents:
                    raise Exception(_("Missing argument in template: ") + k)
                if not isinstance(contents[k], v):
                    raise Exception(_("Argument has wrong type: ") + k +
                                    _(" Expected: ") + str(v) +
                                    _(" Got: ") + str(type(contents[k])))
        except Exception as e:
            raise YAMLTemplateInvalidException(e.args[0])

        name = contents["name"]
        if len(name) < 1:
            raise YAMLTemplateInvalidException(_("Empty name specified"))

        return contents

    @staticmethod
    def get_available_templates() -> Dict[str, str]:
        """
        :return: dict A list of available template files a a dictionary of
                      {template_name: template_path}
        """
        template_files = dict({})
        for dirname, sdn, filenames in os.walk(
                g._config["SURVEY_TEMPLATE_PATH"]):
            for filename in filenames:
                abspath = os.path.join(dirname, filename)
                try:
                    contents = Questionnaire.parse_yaml(abspath)
                except (YAMLTemplateInvalidException, IOError):
                    continue
                template_files[contents["name"]] = abspath
        return template_files

    @staticmethod
    def from_yaml(path_to_yaml: str) -> "Questionnaire":
        """
        Factory method for creating a Questionnaire from a YAML file.
        :param path_to_yaml: str Path to the YAML file to parse
        :return: Questionnaire The newly created Questionnaire
        """
        contents = Questionnaire.parse_yaml(path_to_yaml)
        questionnaire = Questionnaire(name=contents["name"],
                                      description=contents["description"])
        for group_name, question_texts in contents["questions"].items():
            question_group = QuestionGroup(name=group_name,
                                           questionnaire=questionnaire)
            for text in question_texts:
                Question(text=text, question_group=question_group)
            db.session.add(questionnaire)

        return questionnaire
