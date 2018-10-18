from logging.handlers import SMTPHandler

from flask import Flask, request, g
import logging

from framework import get_client_ip

__author__ = "Noah Hummel"


class LogFormatter(logging.Formatter):
    """
    A custom Formatter for logs.
    Injects additional information into the record.
    """
    def format(self, record):
        record.url = request.url
        record.method = request.method
        record.remote_addr = get_client_ip()
        if getattr(g, "_current_user", None) is not None:
            record.current_user = str(g._current_user)
        else:
            record.current_user = "Anonymous"
        return super().format(record)


def configure_loggers(app: Flask, default_handler: logging.Handler) -> None:
    """
    Adds logging handlers to the app instance and
    configures log formatting.
    :param default_handler:
    :param app: The flask app instance.
    """
    mail_handler = SMTPHandler(
        mailhost=(app.config["SMTP_SERVER"], app.config["SMTP_PORT"]),
        fromaddr=app.config["SMTP_FROM_ADDRESS"],
        toaddrs=[app.config["ADMIN_EMAIL"]],
        subject='[Survey Tool] Application Error',
        credentials=(app.config["SMTP_FROM_ADDRESS"], app.config["SMTP_PASSWORD"]),
        secure=()
    )
    log_formatter = LogFormatter(
        '[%(asctime)s] %(levelname)s during %(method)s %(url)s as %(current_user)s@%(remote_addr)s in %(module)s: %(message)s'
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(log_formatter)
    default_handler.setFormatter(log_formatter)
    if not app.config['DEBUG']:
        # only use logging via email for production instances
        app.logger.addHandler(mail_handler)
