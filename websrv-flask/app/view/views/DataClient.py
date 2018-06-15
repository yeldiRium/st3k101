from typing import Dict, Any

from model.SQLAlchemy.models.DataClient import DataClient
from view.View import View


class LegacyView(View):

    @staticmethod
    def render(obj: DataClient) -> Dict[Any, Any]:
        return {
            'class': 'model.DataClient.DataClient',
            'uuid': obj.id,
            'fields': {
                'email': obj.email,
                'locale_name': obj.language.name
            }
        }

