"""
This file contains all the setup logic for the flask.app.
Wherever the app instance is needed (db, api), it is imported from here. 
"""
from logging.handlers import SMTPHandler
from flask import Flask, g
from flask_babel import Babel
import logging

from framework.config import get_config_from_envvars

__author__ = "Noah Hummel"


app = Flask(__name__)


# Setup of flask environment
app.config.from_envvar('FLASK_CONFIG_PATH')  # this path is set in Dockerfile
app.config.update(**get_config_from_envvars())

# Setup of logging for critical errors, critical errors are logged by email
# For configuration, see flask.cfg
mail_handler = SMTPHandler(
    mailhost=(app.config["SMTP_SERVER"], app.config["SMTP_PORT"]),
    fromaddr=app.config["SMTP_FROM_ADDRESS"],
    toaddrs=[app.config["ADMIN_EMAIL"]],
    subject='[Survey Tool] Application Error',
    credentials=(app.config["SMTP_FROM_ADDRESS"], app.config["SMTP_PASSWORD"]),
    secure=()
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(mail_handler)


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
