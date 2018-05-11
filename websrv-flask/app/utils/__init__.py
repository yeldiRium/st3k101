import os
import re

from flask import g

__author__ = "Noah Hummel, Hannes Leutloff"


def generate_verification_token() -> str:
    """
    Helper function to generate a random string that is used as verification
    token at survey submission.
    :return: str A random string of length VERIFICATION_HASH_LENGTH
    """
    verification_hash_length = g._config["VERIFICATION_HASH_LENGTH"]
    some_data = os.urandom(verification_hash_length).hex()
    return some_data


def generate_verification_url(endpoint: str, token: str) -> str:
    """
    Given a verification token and verification endpoint, generates an url 
    pointing to the service.
    :param endpoint: str The /path/to/verification_endpoint
    :param token: str The verification token
    :return: str The url to the verification service
    """
    return "http://{}{}/{}".format(
        g._config["DOMAIN_NAME"],
        endpoint,
        token
    )


def generate_questionnaire_url(questionnaire_uuid: str) -> str:
    """
    Given a questionnaire uuid, generates an url pointing to the survey frontend
    of the given questionnaire.
    :param questionnaire_uuid: str The uuid of the Questionnaire in question
    :return: str The url of the questionnaire
    """
    return "http://{}{}/{}".format(
        g._config["DOMAIN_NAME"],
        "/survey",
        questionnaire_uuid
    )


def check_color(color: str) -> None:
    """
    A helper function to check the validity of hex color codes. Raises
    ValueError if color format is invalid.
    :param color: str The hex color code to check
    :return: None
    """
    regex = re.compile(r'^#[0-9a-fA-F]{6}$')
    if regex.match(color) is None:
        raise ValueError("'{}' is not a well formatted color value. It must be "
                         "a hex-string beginning with #.".format(color))