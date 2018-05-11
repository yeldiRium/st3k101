from typing import Dict, Any

from model.SQLAlchemy.models.DataSubject import DataSubject
from view.View import View


class LegacyView(View):

    @staticmethod
    def render(obj: DataSubject) -> Dict[Any, Any]:
        return {
            'class': 'model.DataSubject.DataSubject',
            'uuid': obj.id,
            'fields': {
                'email': obj.email,
                'locale_name': obj.language.name
            }
        }