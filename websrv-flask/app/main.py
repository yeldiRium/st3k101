from flask import Flask
from memcache import Client

app = Flask(__name__)

@app.route("/")
def hello():
    return "Bring caffeine."