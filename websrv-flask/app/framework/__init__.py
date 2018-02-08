from typing import Any

from flask import request, make_response, jsonify


def get_client_ip():
    """
    Returns the client's IP address. Also takes into account that this app will be behind a proxy,
    because it will be deployed with docker. It does this by checking the X-Forwarded-For http header attribute
    which is set by in-between proxies.
    :return: str The client's IP
    """
    return request.headers.get('X-Forwarded-For', request.remote_addr)


def classname(o):
    """
    Resolves to model.modulename.classname
    :param o: object
    :return: str
    """
    return str(o.__class__)[8:-2]


def make_error(message: Any, status_code: int=400):
    return make_response(jsonify({
        "result": "error",
        "error": message
    }), status_code)
