from flask import Flask
from memcache import Client

app = Flask(__name__)

@app.route("/")
def hello():

    memc = Client("memcached", debug=1)

    if not memc.get("test"):
        return "Visit again"

    memc.set("test", True)  # FIXME

    return "memcached working"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)