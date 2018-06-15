from model.SQLAlchemy.models.QAC.QACCheckboxParameter import QACCheckboxParameter
from view.View import View
from view.views.LegacyShims import legacy_render_data_string


class LegacyView(View):

    @staticmethod
    def render(obj: QACCheckboxParameter):
        return {
            'class': 'model.query_access_control.QACCheckboxParameter.QACCheckboxParameter',
            'uuid': obj.id,
            'fields': {
                'name': legacy_render_data_string(obj.name_msgid),
                'description': legacy_render_data_string(obj.description),
                'value': obj.value
            }
        }
