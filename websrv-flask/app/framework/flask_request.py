from functools import wraps
from typing import List, Tuple, Any

from flask import request

from framework import make_error
from framework.internationalization import _

__author__ = "Noah Hummel, Hannes Leutloff"


def expect(*arguments: List[Tuple[str, type]]):
    """
    A decorator for flask's @app.route decorator, which takes a list of 
    expected request parameters and their types.
    When a request is served, this decorator will parse the expected arguments 
    for the decorated endpoint from the json body of the request.
    It will then pass the arguments as keyword parameters to the endpoint
    function.
    If an expected parameter is not found or has the wrong type, a
    BAD_REQUEST response is automatically served without executing the endpoint
    function.
    
    :param arguments: List[Tuple[str, type]] A list of tuples 
                                             (arg_name, arg_type)
    """

    def wrapper(function):

        @wraps(function)
        def wrapped(*args, **kwargs):

            for arg_name, arg_type in arguments:
                data = request.get_json()
                if data is None or arg_name not in data:
                    return make_error(
                        _("Missing parameter ") + "'{}'".format(arg_name),
                        400
                    )

                argument = data[arg_name]

                if (arg_type is not None) and (arg_type is not Any):
                    try:
                        argument = arg_type(argument)
                    except:
                        return make_error(
                            _("Wrong argument type ") + "'{}'".format(arg_name),
                            400
                        )

                kwargs[arg_name] = argument

            return function(*args, **kwargs)

        return wrapped

    return wrapper


def expect_optional(*arguments: List[Tuple[str, type]]):
    """
    A decorator for flask's @app.route decorator, which takes a list of 
    optional request parameters and their types.
    When a request is served, this decorator will parse the optional arguments 
    for the decorated endpoint from the json body of the request.
    It will then pass the arguments as keyword parameters to the endpoint
    function.
    If an optional parameter has the wrong type, a BAD_REQUEST response is 
    automatically served without executing the endpoint function.

    :param arguments: List[Tuple[str, type]] A list of tuples 
                                             (arg_name, arg_type)
    """

    def wrapper(function):

        @wraps(function)
        def wrapped(*args, **kwargs):

            for arg_name, arg_type in arguments:
                data = request.get_json()
                if data is None or arg_name not in data:
                    continue

                argument = data[arg_name]

                if argument is None:
                    continue

                if (arg_type is not None) and (arg_type is not Any):
                    try:
                        argument = arg_type(argument)
                    except:
                        return make_error(
                            _("Wrong argument type ") + "'{}'".format(arg_name),
                            400
                        )

                kwargs[arg_name] = argument

            return function(*args, **kwargs)

        return wrapped

    return wrapper
