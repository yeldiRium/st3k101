from functools import wraps
from typing import List, Tuple, Any

from flask import request

from framework import make_error
from framework.internationalization import _


def expect(*arguments: List[Tuple[str, type]]):

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

    def wrapper(function):

        @wraps(function)
        def wrapped(*args, **kwargs):

            for arg_name, arg_type in arguments:
                data = request.get_json()
                if data is None or arg_name not in data:
                    continue

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
