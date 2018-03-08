import os

from flask import g


def generate_verification_token():
    verification_hash_length = g._config["VERIFICATION_HASH_LENGTH"]
    some_data = os.urandom(verification_hash_length).hex()
    return some_data


def generate_verification_url(endpoint, token):
    return "http://{}{}/{}".format(
        g._config["DOMAIN_NAME"],
        endpoint,
        token
    )