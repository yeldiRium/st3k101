import redis
from flask import Flask

__author__ = "Noah Hummel"

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')


redis_connection_pool = redis.ConnectionPool(
    host=app.config['REDIS_URL'],
    port=app.config['REDIS_PORT'],
    db=app.config['APPLICATION_REDIS_DB']
)
