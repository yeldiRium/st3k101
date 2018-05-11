from model.SQLAlchemy.models.QuestionGroup import QuestionGroup
from view.View import View
from view.views.LegacyShims import legacy_render_i15d
from view.views.Question import LegacyView as Question_LegacyView


class LegacyView(View):

    @staticmethod
    def render(obj: QuestionGroup):
        return {
            'class': 'model.QuestionGroup.QuestionGroup',
            'uuid': obj.id,
            'fields': {
                'color': obj.color,
                'text_color': obj.text_color,
                'name': legacy_render_i15d(obj.name_translations),
                'questions': Question_LegacyView.expand(obj.questions)
            }
        }
