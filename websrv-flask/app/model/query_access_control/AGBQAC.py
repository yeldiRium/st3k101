from typing import List, Dict

from model.query_access_control.QACModule import QACModule
from flask import request, render_template_string


class AGBQAC(QACModule):
    def get_required_config_fields(self) -> List[str]:
        return []

    def get_name(self) -> str:
        return "AGBQAC"

    def get_survey_template(self, errors: Dict[str, str]) -> str:
        return render_template_string("QAC_AGB.html", error=True)

    def control(self) -> Dict[str, str]:
        if 'agb' not in request.form or not request.form['agb']:
            return {
                'agb': 'Please accept.'
            }
        else:
            return {}
