from flask import Flask

__author__ = "Noah Hummel"

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')
