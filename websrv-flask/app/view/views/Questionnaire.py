from model.SQLAlchemy.models.Questionnaire import Questionnaire
from view.View import View
from view.views.LegacyShims import legacy_render_i15d
from view.views.QuestionGroup import LegacyView as QuestionGroup_LegacyView


class LegacyView(View):

    @staticmethod
    def render(obj: Questionnaire):
        return {
            'class': 'model.Questionnaire.Questionnaire',
            'uuid': obj.id,
            'fields': {
                'answer_count': obj.answer_count,
                'description': legacy_render_i15d(obj.description_translations),
                'name': legacy_render_i15d(obj.name_translations),
                'original_locale': obj.original_language.name,
                'published': obj.published,
                'question_count': obj.question_count,
                'questiongroups': QuestionGroup_LegacyView.expand(obj.question_groups)
            }
        }
