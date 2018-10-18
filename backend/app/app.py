"""
This file contains all the setup logic for the flask.app.
Wherever the app instance is needed (db, api), it is imported from here. 
"""
from flask import Flask, g
from flask.logging import default_handler
from flask_babel import Babel

from framework.logging import configure_loggers
from framework.config import get_config_from_envvars

__author__ = "Noah Hummel"


app = Flask(__name__)


# Setup of flask environment
app.config.from_envvar('FLASK_CONFIG_PATH')  # this path is set in Dockerfile
app.config.update(**get_config_from_envvars())

# Setup of logging for critical errors, critical errors are logged by email
# For configuration, see flask.cfg
configure_loggers(app, default_handler)

# Setup of flask_babel to ba able to use gettext() for translating strings
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Uses the sanest locale according to g._locale, that is set in before_request
    :return: str The locale that should be used for the current request
    by babel
    """
    return g._language.name


@babel.timezoneselector
def get_timezone():
    """
    Returns the timezone flask_babel will use.
    We could make an effort here and select one based on locale or browser
    settings, but we don't handle time information, so we just use one
    fixed timezone that is set in flask.cfg
    :return: str The timezone set in flask.cfg
    """
    return g._config["TIMEZONE"]
