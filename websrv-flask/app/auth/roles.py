from enum import IntEnum
from functools import wraps
from typing import List, Union, Tuple

from flask import g

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


def needs_role(*roles: List[Union[Role, Tuple[Role]]]):

    def wrapper(route):

        @wraps(route)
        def wrapped(*args, **kwargs):
            user = g._current_user
            if fulfills_role(user, *roles):
                return route(*args, **kwargs)
            else:
                return make_error(_("Forbidden"), 403)

        return wrapped

    return wrapper
