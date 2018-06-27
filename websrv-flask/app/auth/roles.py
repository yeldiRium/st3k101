from enum import IntEnum
from functools import wraps
from typing import List, Union, Tuple

from flask import g
from flask_restful import abort

from framework import make_error
from framework.internationalization import _

__author__ = "Noah Hummel"


class Role(IntEnum):
    Root = 0
    Admin = 10
    Contributor = 20
    User = 30


def fulfills_role(data_client, *roles: List[Union[Role, Tuple[Role]]]):
    access_allowed = True
    if not data_client:
        return False

    user_roles = data_client.roles
    for role in roles:
        if isinstance(role, Role):
            access_allowed &= (role in user_roles)
        elif type(role) == tuple:
            access_allowed &= any(sr in user_roles for sr in role)

    return access_allowed


def current_has_role(*roles: Role):
    if not g._current_user:
        return False
    return any((role in g._current_user.roles for role in roles))


def current_has_minimum_role(role: Role):
    user = g._current_user
    if not user:
        return False
    highest_role = sorted(user.roles)[0]
    return highest_role <= role


def needs_role(*roles: List[Union[Role, Tuple[Role]]]):

    def wrapper(route):

        @wraps(route)
        def wrapped(*args, **kwargs):
            user = g._current_user
            if fulfills_role(user, *roles):
                return route(*args, **kwargs)
            else:
                abort(401)

        return wrapped

    return wrapper


def needs_minimum_role(role: Role):

    def wrapper(route):

        @wraps(route)
        def wrapped(*args, **kwargs):
            user = g._current_user
            if not user:
                return abort(401)
            highest_role = sorted(user.roles)[0]

            if highest_role <= role:
                return route(*args, **kwargs)
            else:
                return abort(401)

        return wrapped

    return wrapper
