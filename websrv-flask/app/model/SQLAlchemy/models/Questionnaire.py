import os
from abc import abstractmethod
from typing import Dict, Optional, Any

import yaml
from deprecated import deprecated
from flask import g

from auth.users import current_user
from framework.exceptions import QACAlreadyEnabledException, YAMLTemplateInvalidException, BusinessRuleViolation
from framework.internationalization import _, __
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingType, TrackingArg, relationship_updated, item_deleted
from model.SQLAlchemy.models.TrackerEntry import RelationshipAction
from model.SQLAlchemy import db, MUTABLE_HSTORE, translation_hybrid
from model.SQLAlchemy.models.Dimension import Dimension, ConcreteDimension, ShadowDimension
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from model.SQLAlchemy.models.QAC.QACModules.EMailVerificationQAC import EMailVerificationQAC
from model.SQLAlchemy.models.QAC.QACModules.TOSQAC import TOSQAC
from model.SQLAlchemy.models.Question import Question, ShadowQuestion, ConcreteQuestion
from model.SQLAlchemy.models.QuestionResult import QuestionResult
from model.SQLAlchemy.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


class Questionnaire(SurveyBase):
    id = db.Column(db.Integer, db.ForeignKey(SurveyBase.id), primary_key=True)

    __tablename__ = 'questionnaire'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    published = db.Column(db.Boolean, nullable=False, default=False)
    allow_embedded = db.Column(db.Boolean, nullable=False, default=False)
    xapi_target = db.Column(db.String(512))

    # relationships
    dimensions = db.relationship(
        'Dimension',
        backref='questionnaire',
        cascade='all, delete-orphan',
        foreign_keys=[Dimension.questionnaire_id]
    )
    qac_modules = db.relationship(
        'QACModule',
        backref='questionnaire',
        cascade='all, delete-orphan',
        foreign_keys=[QACModule.questionnaire_id]
    )

    tracker_args = {
        __('name'): [
            TrackingType.TranslationHybrid,
            TrackingArg.Accumulate
        ],
        __('description'): [
            TrackingType.TranslationHybrid,
            TrackingArg.Accumulate
        ],
        __('randomize_question_order'): [
            TrackingType.Primitive,
            TrackingArg.Accumulate
        ]
    }

    def __init__(self, **kwargs):
        super(Questionnaire, self).__init__(**kwargs)
        self.qac_modules = [TOSQAC(), EMailVerificationQAC()]

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def name_translations(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description_translations(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        raise NotImplementedError

    @property
    def question_count(self) -> int:
        """
        :return: The number of questions associated with the Questionnaire.
        """
        count = 0
        for dim in self.dimensions:
            count += len(dim.questions)
        return count

    @property
    def answer_count(self) -> int:
        """
        :return: The number of verified answers for the Questionnaire.
        """
        count = 0
        for qg in self.question_groups:
            for q in qg.questions:
                verified_results = QuestionResult.query.\
                    filter_by(question=q, verified=True).all()
                count += len(verified_results)
        n_questions = self.question_count
        if n_questions < 1:
            n_questions = 1
        return count // n_questions

    def new_dimension(self, name: str) -> ConcreteDimension:
        if not isinstance(self, ConcreteQuestionnaire):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        dimension = ConcreteDimension(name)
        self.dimensions.append(dimension)

        for copy in self.copies:
            s_dimension = ShadowDimension(dimension)
            s_dimension.owners = copy.owners
            copy.dimensions.append(s_dimension)

        relationship_updated.send(
            self,
            relationship_name=__('Dimension'),
            action=RelationshipAction.Add,
            related_object=dimension,
            person=current_user()
        )

        return dimension

    def add_shadow_dimension(self, concrete_dimension: ConcreteDimension)\
            -> ShadowDimension:
        if not isinstance(self, ConcreteQuestionnaire):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        dimension = ShadowDimension(concrete_dimension)
        self.dimensions.append(dimension)

        for copy in self.copies:
            s_dimension = ShadowDimension(concrete_dimension)
            s_dimension.owners = copy.owners
            copy.dimensions.append(s_dimension)

        relationship_updated.send(
            self,
            relationship_name=__('Dimension'),
            action=RelationshipAction.Add,
            related_object=dimension,
            person=current_user()
        )

        return dimension

    def remove_dimension(self, dimension):
        if not isinstance(self, ConcreteQuestionnaire):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        if dimension not in self.dimensions:
            raise KeyError("Question not in Dimension.")
        for copy in [*self.copies, self]:
            for s_dimension in copy.dimensions:
                if not isinstance(s_dimension, ShadowDimension):
                    continue
                if s_dimension.concrete_id == dimension.id:
                    db.session.delete(s_dimension)

        relationship_updated.send(
            self,
            relationship_name=__('Dimension'),
            action=RelationshipAction.Remove,
            related_object=dimension.name,
            person=current_user()
        )

        self.dimensions.remove(dimension)

    def delete(self):
        item_deleted.send(self, current_user())

        for copy in self.copies:
            q = ConcreteQuestionnaire.from_shadow(copy)
            db.session.add(q)
        for copy in self.copies:
            db.session.delete(copy)
        db.session.delete(self)

    def add_qac_module(self, qac_module: QACModule):
        if qac_module.qac_id in (qm.qac_id for qm in self.qac_modules):
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

    @staticmethod
    @deprecated(version='2.0', reason='YAML templates will be removed in version 2.0')
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
    @deprecated(version='2.0', reason='YAML templates will be removed in version 2.0')
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
    @deprecated(version='2.0', reason='YAML templates will be removed in version 2.0')
    def from_yaml(path_to_yaml: str) -> "Questionnaire":
        """
        Factory method for creating a Questionnaire from a YAML file.
        :param path_to_yaml: str Path to the YAML file to parse
        :return: Questionnaire The newly created Questionnaire
        """
        contents = Questionnaire.parse_yaml(path_to_yaml)
        questionnaire = Questionnaire(name=contents["name"],
                                      description=contents["description"])
        for dimension_name, question_texts in contents["questions"].items():
            dimension = Dimension(name=dimension_name,
                                  questionnaire=questionnaire)
            for text in question_texts:
                Question(text=text, dimension=dimension)
            db.session.add(questionnaire)

        return questionnaire


class ConcreteQuestionnaire(Questionnaire):
    id = db.Column(db.Integer, db.ForeignKey(Questionnaire.id), primary_key=True)

    __tablename__ = 'concrete_questionnaire'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    name_translations = db.Column(MUTABLE_HSTORE)
    name = translation_hybrid(name_translations)
    description_translations = db.Column(MUTABLE_HSTORE)
    description = translation_hybrid(description_translations)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)

    def __init__(self, name, description, **kwargs):
        self.original_language = g._language
        super(ConcreteQuestionnaire, self).__init__(name=name,
                                                    description=description,
                                                    **kwargs)

    @staticmethod
    def from_shadow(shadow):
        q = ConcreteQuestionnaire("", "")
        q.name_translations = shadow.name_translations
        q.description_translations = shadow.description_translations
        q.original_language = shadow.original_language
        q.published = shadow.published
        q.allow_embedded = shadow.allow_embedded
        q.xapi_target = shadow.xapi_target
        q.owners = shadow.owners

        for s_dimension in shadow.dimensions:
            c_dimension = ConcreteDimension.from_shadow(s_dimension)
            q.dimensions.append(c_dimension)

        return q


class ShadowQuestionnaire(Questionnaire):
    id = db.Column(db.Integer, db.ForeignKey(Questionnaire.id), primary_key=True)

    __tablename__ = 'shadow_questionnaire'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _referenced_object_id = db.Column(db.Integer,
                                      db.ForeignKey(ConcreteQuestionnaire.id))
    _referenced_object = db.relationship(ConcreteQuestionnaire,
                                         foreign_keys=[_referenced_object_id],
                                         backref='copies')

    def __init__(self, questionnaire, **kwargs):
        super(ShadowQuestionnaire, self).__init__(**kwargs)
        self._referenced_object = questionnaire

        for dimension in questionnaire.dimensions:
            if not isinstance(dimension, ConcreteDimension):
                dimension = dimension.concrete
            s_dimension = ShadowDimension(dimension)
            self.dimensions.append(s_dimension)
            for question in dimension.questions:
                if not isinstance(question, ConcreteQuestion):
                    question = question.concrete
                s_question = ShadowQuestion(question)
                s_dimension.questions.append(s_question)

    @property
    def concrete_id(self):
        if self._referenced_object is None:
            return None
        return self._referenced_object.id

    @property
    def concrete(self):
        if self._referenced_object is None:
            return None
        return self._referenced_object

    @property
    def name(self) -> str:
        return self._referenced_object.name

    @property
    def name_translations(self) -> Dict[str, str]:
        return self._referenced_object.name_translations

    @property
    def description(self) -> str:
        return self._referenced_object.description

    @property
    def description_translations(self) -> Dict[str, str]:
        return self._referenced_object.description_translations

    @property
    def original_language(self) -> BabelLanguage:
        return self._referenced_object.original_language
