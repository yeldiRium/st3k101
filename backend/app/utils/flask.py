from flask import g
from contextlib import contextmanager

from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


def setup_app_context(app, language=None, user=None):
    """
    Sets request-global variables needed for the app to function.
    Normally, these variables are set before_request. This
    method can be used to populate the app context with sane dummy
    values. Used for creating an app context in cli commands.
    """
    g._config = app.config
    if language is None or language not in BabelLanguage:
        g._language = BabelLanguage[app.config['BABEL_DEFAULT_LOCALE']]
    else:
        g._language = language
    g._current_user = user  # TODO: what should be the default value?


@contextmanager
def context_language(language: BabelLanguage):
    previous_language = g._language
    g._language = language
    yield
    g._language = previous_language