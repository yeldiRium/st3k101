from model.SQLAlchemy.models.Survey import Survey
from view.View import View
from view.views.LegacyShims import legacy_render_i15d
from view.views.Questionnaire import LegacyView as Questionnaire_LegacyView


class LegacyView(View):

    @staticmethod
    def render(obj: Survey):
        return {
            'class': 'model.Survey.Survey',
            'uuid': obj.id,
            'fields': {
                'date_created': obj.date_created,
                'name': legacy_render_i15d(obj.name_translations),
                'original_locale': obj.original_language.name,
                'questionnaires': Questionnaire_LegacyView.expand(obj.questionnaires)
            }
        }