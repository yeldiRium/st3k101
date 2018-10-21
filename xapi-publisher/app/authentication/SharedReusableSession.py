import json
from typing import Dict, Any, Type

import redis

import app
from authentication.methods.AuthenticationMethod import AuthenticationMethod

__author__ = "Noah Hummel"


class StaleSession(Exception):
    pass


class SharedReusableSession(object):
    r = redis.StrictRedis(connection_pool=app.redis_connection_pool)

    def __init__(self, handle):
        print("[SESSION] Trying handle {} ...".format(handle))
        self.__handle = handle
        if self.r.get(handle) is None:
            print("[SESSION] Handle {} is stale.".format(handle))
            raise StaleSession
        else:
            print("[SESSION] State for handle {} exists!".format(handle))

    @property
    def handle(self) -> int:
        return self.__handle

    @property
    def state(self) -> dict:
        print("[SESSION] Accessing state of {} ...".format(self.handle))
        state = json.loads(self.r.get(self.handle))
        if state is None:
            print("[SESSION] Handle {} is stale.".format(self.handle))
            raise StaleSession
        return state

    def make_stale(self):
        print("[SESSION] Marking {} as stale.".format(self.handle))
        self.r.delete(self.handle)

    @staticmethod
    def get_handle(method: Type[AuthenticationMethod], destination: str, parameters: dict) -> int:
        return hash((method.__name__, destination,  frozenset(parameters.items())))

    @staticmethod
    def validate_parameters(method: Type[AuthenticationMethod], parameters: Dict[str, Any]) -> None:
        required_parameters = set(method.required_parameters.keys())
        for parameter_name, parameter_value in parameters.items():
            expected_type = method.required_parameters.get(parameter_name, None)
            actual_type = type(parameter_value)
            if expected_type is None:
                raise ValueError('Unexpected authentication parameter "{}".'.format(parameter_name))
            if actual_type != expected_type:
                raise ValueError('Type mismatch for parameter "{}". Expected "{}", git "{}"'.format(
                    parameter_name, expected_type, actual_type))
            required_parameters.discard(parameter_name)
        if len(required_parameters) != 0:
            raise ValueError("Missing parameters: {}".format(required_parameters))

    @staticmethod
    def new(method: Type[AuthenticationMethod], destination: str, parameters: dict) -> "SharedReusableSession":
        SharedReusableSession.validate_parameters(method, parameters)
        handle = SharedReusableSession.get_handle(method, destination, parameters)
        state = method.create_session(parameters)
        if not state:
            state = dict({})
        SharedReusableSession.__set_state(handle, state)
        print("[SESSION] New state with handle {} created.".format(handle))
        return SharedReusableSession(handle)

    @staticmethod
    def __set_state(handle, state: dict):
        print("[SESSION] Setting state for handle {} ...".format(handle))
        serialized_state = json.dumps(state)
        SharedReusableSession.r.set(handle, serialized_state)
