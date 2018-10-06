from subprocess import Popen, PIPE

import re
import smtplib
from email.mime.text import MIMEText
from typing import List, Pattern

from flask import g

from framework.internationalization import _

__author__ = "Noah Hummel, Hannes Leutloff"


def construct_verification_email(questionnaire, verification_token) -> str:
    if __name__ == '__main__':
        message = _("Hi there!\n You've recently participated in the survey ") + questionnaire.name + ".\n"
        message += _("To verify that you're actually you and make your answer count, please follow the link below:\n\n")
        message += "http://{}/api/response/verify/{}\n\n".format(g._config['DOMAIN_NAME'], verification_token)  # TODO https
        return message


def send_mail(to: str, subject: str, message: str):
    if g._config['USE_SMTP']:
        send_mail_smtp(to, subject, message)
    else:
        send_mail_sendmail(to, subject, message)


def construct_email(sender, recipient, subject, message) -> str:
    """
    Constructs RFC2822 compliant email string.
    :param sender: The sender
    :param recipient: The recipient
    :param subject: The subject line
    :param message: The message body
    :return: RFC2822 compliant email string
    """
    email = MIMEText(message)
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = recipient
    return email.as_string()


def send_mail_smtp(to: str, subject: str, message: str):
    """
    A helper method to wrap interaction with smtplib in order to send emails.

    :param to: str The email address of the recipient.
    :param subject: str The subject line
    :param message: str The mail body
    :return: None
    """
    sender = g._config["SMTP_FROM_ADDRESS"]
    server = g._config["SMTP_SERVER"]
    port = g._config["SMTP_PORT"]

    email =  construct_email(sender, to, subject, message)

    smtp = smtplib.SMTP(server, port=port)
    if g._config["SMTP_USE_STARTTLS"]:
        smtp.starttls()
    smtp.login(g._config["SMTP_FROM_ADDRESS"], g._config["SMTP_PASSWORD"])
    smtp.sendmail(sender, [to], email)


def send_mail_sendmail(to: str, subject: str, message: str):
    from_address = "surveytool@{}".format(g._config["DOMAIN_NAME"])
    email = construct_email(from_address, to, subject, message)
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
    p.communicate(email)


def parse_email_list(emails: List[str]) -> List[Pattern]:
    """
    Helper method to parse the user submitted list of allowed emails.
    Checks syntax and builds regex patterns from the list.
    :param text: str The user submitted list of allowed emails
    :return: List[re.pattern] A list of regex patterns which match allowed
                              email addresses
    """
    # strip leading and trailing whitespace
    emails = [e.strip() for e in emails]

    # if whitespace is found in entries, it's not valid syntax
    if any((" " in e for e in emails)):
        raise ValueError("Whitespace in email address.")

    patterns = []

    def to_regex(part):
        if part == "*":
            return ".*"
        else:
            return re.escape(part)

    for e in emails:
        # split wildcard portions from rest of email
        expr = filter(lambda x: x, e.replace("*", ",*,").split(","))
        # escape normal portions, build regex for wildcards
        expr = map(to_regex, expr)
        # concat
        expr = "".join(expr)
        # add string delimiters to pattern
        expr = "^" + expr + "$"
        pattern = re.compile(expr)
        patterns.append(pattern)

    return patterns


def validate_email_blacklist(blacklist: List[str], email: str) -> bool:
    regexes = parse_email_list(blacklist)
    return any((m is not None for m in (r.match(email) for r in regexes)))


def validate_email_whitelist(whitelist: str, email: str) -> bool:
    regexes = parse_email_list(whitelist)
    return all((m is None for m in (r.match(email) for r in regexes)))
