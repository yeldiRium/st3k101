from typing import Dict

from app import app
from framework.internationalization import _


def legacy_render_i15d(text_translations: Dict[str, str]):
    default_locale = app.config['BABEL_DEFAULT_LOCALE']
    if default_locale not in text_translations:
        default_locale = list(text_translations.keys())[0]

    return {
        'class': 'model.I15dString.I15dString',
        'uuid': None,
        'fields': {
            'default_locale': default_locale,
            'locales': text_translations
        }
    }


def legacy_render_data_string(msgid: str) -> Dict[str, str]:
    return {
        'msgid': msgid,
        'text': _(msgid)
    }
