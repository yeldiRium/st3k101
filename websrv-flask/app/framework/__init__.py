from typing import Any

from flask import request, make_response, jsonify, Response

__author__ = "Noah Hummel, Hannes Leutloff"


def get_client_ip() -> str:
    """
    Returns the client's IP address. Also takes into account that this app will
    be behind a proxy, because it will be deployed with docker. It does this by 
    checking the X-Forwarded-For http header attribute which is set by nginx.
    :return: str The client's IP
    """
    return request.headers.get('X-Forwarded-For', request.remote_addr)


def classname(o: object) -> str:
    """
    Returns model.modulename.classname
    :param o: object The Object whose class path to get
    :return: str The class path for the object#s class
    """
    return str(o.__class__)[8:-2]


def make_error(message: Any, status_code: int=400) -> Response:
    """
    Helper function to return a json-body error response through the API.
    
    Format of response:
    
        {
            "message": message
        }
    
    :param message: Any An error message
    :param status_code: int The HTTP status code to use for the response
    :return: Response The error response
    """
    return make_response(jsonify({
        "message": message
    }), status_code)
