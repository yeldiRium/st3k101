from model.SQLAlchemy.models.QAC.QACI15dTextParameter import QACI15dTextParameter
from view.View import View
from view.views.LegacyShims import legacy_render_i15d, legacy_render_data_string


class LegacyView(View):

    @staticmethod
    def render(obj: QACI15dTextParameter):
        return {
            'class': 'model.query_access_control.QACI15dTextParameter.QACI15dTextParameter',
            'uuid': obj.id,
            'fields': {
                'name': legacy_render_data_string(obj.name_msgid),
                'description': legacy_render_data_string(obj.description_msgid),
                'text': legacy_render_i15d(obj.text_translations)
            }
        }
