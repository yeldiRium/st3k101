from model.SQLAlchemy.models.Question import Question
from view.View import View
from view.views.LegacyShims import legacy_render_i15d


class LegacyView(View):

    @staticmethod
    def render(obj: Question):
        return {
            'class': 'model.Question.Question',
            'uuid': obj.id,
            'fields': {
                'text': legacy_render_i15d(obj.text_translations)
            }
        }
