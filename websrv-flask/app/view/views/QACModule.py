from model.SQLAlchemy.models.QAC.QACCheckboxParameter import QACCheckboxParameter
from model.SQLAlchemy.models.QAC.QACI15dTextParameter import QACI15dTextParameter
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from model.SQLAlchemy.models.QAC.QACTextParameter import QACTextParameter
from view.View import View
from view.views.LegacyShims import legacy_render_data_string

from view.views.QACTextParameter import LegacyView as QACTextParameter_LegacyView
from view.views.QACI15dTextParameter import LegacyView as QACI15dTextParameter_LegacyView
from view.views.QACCheckboxParameter import LegacyView as QACCheckboxParameter_LegacyView


class LegacyView(View):

    @staticmethod
    def render(obj: QACModule):

        parameters = []
        for p in obj.parameters:
            if isinstance(p, QACTextParameter):
                the_view = QACTextParameter_LegacyView
            elif isinstance(p, QACI15dTextParameter):
                the_view = QACI15dTextParameter_LegacyView
            elif isinstance(p, QACCheckboxParameter):
                the_view = QACCheckboxParameter_LegacyView
            else:
                continue

            parameters.append(the_view.render(p))

        return {
            'class': 'model.query_access_control.QACModules.{}'.format(obj.qac_id),
            'uuid': obj.id,
            'fields': {
                'name': legacy_render_data_string(obj.qac_id),
                'description': legacy_render_data_string(obj.description_msgid),
                'parameters': parameters
            }
        }