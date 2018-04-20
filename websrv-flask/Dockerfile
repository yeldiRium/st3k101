FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

RUN pip install -r /app/requirements.txt
RUN apt update -y && apt install -y python-mysqldb

WORKDIR /app
RUN pybabel compile -d translations

ENV FLASK_CONFIG_PATH="/app/flask.cfg"
ENV FLASK_APP="main.py"
