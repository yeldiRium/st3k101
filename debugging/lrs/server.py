__author__ = "Noah Hummel"

import pprint
import random

from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def receive_xapi_statements():
    assert request.json is not None

    if random.random() >= 0.8:  # randomly drop statements to simulate flaky network
        abort(400)

    if type(request.json) == list:
        statements = [*request.json]
    else:
        statements = [request.json]

    pp = pprint.PrettyPrinter(compact=True)

    with open('statements.log', 'a') as f:
        for statement in statements:
            f.write(pp.pformat(statement))
            f.write("\n<< EOS\n")

    return "Success."
