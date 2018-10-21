import os

__author__ = "Noah Hummel"


def boolean(value):
    if type(value) is not str:
        raise ValueError("Expected a string!")
    value = value.upper()
    if value not in ["1", "0", "TRUE", "FALSE", "YES", "NO", "Y", "N"]:
        raise ValueError("Not a boolean.")
    return value in ["1", "TRUE", "YES", "Y"]


_config_keys = {
    "LANGUAGE": {
        "type": str,
        "default": "en"
    },
    "TIMEZONE": {
        "type": str,
        "default": "Europe/Berlin"
    },
    "DOMAIN_NAME": {
        "type": str,
        "default": "localhost"
    },
    "ADMIN_EMAIL": {
        "type": str
    },
    "XAPI_DEFAULT_ENDPOINT": {
        "type": str,
        "default": "tla.edutec.guru"
    },
    "TLA_XAPI_ENDPOINT": {
        "type": str
    },
    "TLA_AUTH_ENDPOINT": {
        "type": str
    },
    "TLA_AUTH_USERNAME": {
        "type": str
    },
    "TLA_AUTH_PASSWORD": {
        "type": str
    },
    "SMTP_FROM_ADDRESS": {
        "type": str
    },
    "SMTP_PASSWORD": {
        "type": str
    },
    "SMTP_SERVER": {
        "type": str
    },
    "SMTP_PORT": {
        "type": int,
        "default": 587
    },
    "SMTP_USE_STARTTLS": {
        "type": boolean,
        "default": True
    },
    "DEBUG": {
        "type": boolean,
        "default": False
    }
}


class MissingConfigValueException(Exception):
    def __init__(self, key):
        message = "Missing config value for {}. Please set this value using environment files.".format(key)
        super(MissingConfigValueException, self).__init__(message)


class InvalidConfigValueException(Exception):
    def __init__(self, key, expected_type, value):
        message = "Invalid type for config key {}. Expected {}, but got {}".format(key, expected_type, value)
        super(InvalidConfigValueException, self).__init__(message)


def get_config_from_envvars() -> dict:
    config_values = dict()

    for key, info in _config_keys.items():
        value = os.environ.get(key)
        expected_type: type = info["type"]
        default_value = info.get("default")
        if value is None:
            if default_value is None:
                raise MissingConfigValueException(key)
            value = default_value
        else:
            try:
                value = expected_type(value)
            except ValueError:
                raise InvalidConfigValueException(key, expected_type, value)
        config_values[key] = value

    return config_values
