from flask import Response

from app import app
from transmission import flush

__author__ = "Noah Hummel"


@app.after_request
def after_request(response: Response):
    flush()
    return response

# do not remove this import
import api
