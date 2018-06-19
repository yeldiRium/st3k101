import os
from typing import Tuple

import argon2
from flask import g

import auth
from framework.exceptions import UserExistsException, BadCredentialsException, \
    UserNotLoggedInException
from model.SQLAlchemy import db
from model.SQLAlchemy.models.DataClient import DataClient

__author__ = "Noah Hummel, Hannes Leutloff"


def register(email: str, password: str) -> DataClient:
    """
    Registers a new DataClient.
    Raises UserExistsException, if a user with the given email address already 
    exists.
    :param email: str The email address of the DataClient
    :param password: str The password the DataClient will use to login
    :return: DataClient The resulting DataClient object
    """
    client = DataClient.query.filter_by(email=email).first()
    if client is not None:
        raise UserExistsException(
            "User with email address {} already exists.".format(email)
        )

    client = DataClient(email=email)
    client.password = password
    db.session.add(client)

    return client


def login(email: str, password: str) -> str:
    """
    Logs a DataClient in by checking if the user exists, matching the password 
    hashes and creating a new session token in memcache if authentication is 
    successful. Returns the session token.
    Raises SessionExistsException or BadCredentialsException if appropriate.
    :param email: The email address of the user to log in
    :param password: The plain text password of the user to log in
    :return: The session token for the newly created session
    """
    client = DataClient.query.filter_by(email=email).first()
    if client is None:
        raise BadCredentialsException("User with email {} doesn't exist.".format(email))

    password_hash = argon2.argon2_hash(password, client.password_salt).hex()
    if password_hash != client.password_hash:
        raise BadCredentialsException("Tried to login as {}, but password hashes didn't match.".format(email))

    success = False
    session_token = ""
    while not success:
        session_token = os.urandom(g._config['AUTH_SESSION_TOKEN_LENGTH']).hex()
        success = auth.new_session(session_token, client.id)

    return session_token


def logout():
    """
    Logs out the current user, raises UserNotLoggedInException if the session is already invalid.
    :return: None
    """
    if g._current_user is None:
        raise UserNotLoggedInException()

    if not auth.invalidate(g._current_session_token):
        raise UserNotLoggedInException()


def current_user() -> DataClient:
    return g._current_user
