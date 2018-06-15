from model.SQLAlchemy.models.QAC.QACTextParameter import QACTextParameter
from view.View import View
from view.views.LegacyShims import legacy_render_data_string


class LegacyView(View):

    @staticmethod
    def render(obj: QACTextParameter):
        return {
            'class': 'model.query_access_control.QACTextParameter.QACTextParameter',
            'uuid': obj.id,
            'fields': {
                'name': legacy_render_data_string(obj.name_msgid),
                'description': legacy_render_data_string(obj.description),
                'text': obj.text
            }
        }
