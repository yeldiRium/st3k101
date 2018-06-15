from marshmallow import fields
import re

__author__ = "Noah Hummel"


def email(email_str: str) -> str:
    regex = re.compile(r'^\S+@\S+\.\S\S+$')
    if regex.match(email_str) is None:
        raise ValueError("'{}' is not a valid email address".format(email_str))
    return email_str


def password(password_str: str) -> str:
    regex = re.compile(r'^\S{8,128}$')
    if regex.match(password_str) is None:
        raise ValueError("'{}' is not a valid email address"
                         .format(password_str))

