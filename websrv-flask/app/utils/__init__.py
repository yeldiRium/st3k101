import os

from flask import g


def generate_verification_token():
    """
    Helper function to generate a random string that is used as verification
    token at survey submission.
    :return: str A random string of length VERIFICATION_HASH_LENGTH
    """
    verification_hash_length = g._config["VERIFICATION_HASH_LENGTH"]
    some_data = os.urandom(verification_hash_length).hex()
    return some_data


def generate_verification_url(endpoint, token):
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


def generate_questionnaire_url(questionnaire_uuid):
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