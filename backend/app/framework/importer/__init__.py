from framework.importer.schema.Questionnaire import QuestionnaireImportSchema
from model import db
from model.models.Questionnaire import ConcreteQuestionnaire
from framework.flask import context_language

__author__ = "Noah Hummel"


def import_questionnaires(questionnaires_as_json):
    questionnaires = QuestionnaireImportSchema(many=True).loads(questionnaires_as_json).data
    for questionnaire in questionnaires:
        qn_original_language = questionnaire['original_language']
        qn_original_name = questionnaire['name'][qn_original_language.name]
        qn_original_description = questionnaire['description'][qn_original_language.name]
        with context_language(qn_original_language):
            # switch to original_language to create questionnaire
            new_questionnaire = ConcreteQuestionnaire(qn_original_name,
                                                      qn_original_description)
        new_questionnaire.template = questionnaire['template']
        new_questionnaire.reference_id = questionnaire['reference_id']
        new_questionnaire.name_translations = questionnaire['name']
        new_questionnaire.description_translations = questionnaire['description']

        for dimension in questionnaire['dimensions']:
            dm_original_name = dimension['name'][qn_original_language.name]
            with context_language(qn_original_language):
                new_dimension = new_questionnaire.new_dimension(dm_original_name)
            new_dimension.template = new_questionnaire.template
            new_dimension.reference_id = dimension['reference_id']
            new_dimension.randomize_question_order = dimension['randomize_question_order']
            new_dimension.name_translations = dimension['name']

            for question in dimension['questions']:
                qs_original_text = question['text'][qn_original_language.name]
                qs_original_range_start_label = question['range_start_label'][qn_original_language.name]
                qs_original_range_end_label = question['range_end_label'][qn_original_language.name]
                with context_language(qn_original_language):
                    new_question = new_dimension.new_question(qs_original_text, qs_original_range_start_label,
                                                              qs_original_range_end_label)

                new_question.template = new_questionnaire.template
                new_question.reference_id = question['reference_id']
                new_question.range_start = question['range_start']
                new_question.range_end = question['range_end']
                new_question.text_translations = question['text']
                new_question.range_start_label_translations = question['range_start_label']
                new_question.range_end_label_translations = question['range_end_label']

        db.session.add(new_questionnaire)
