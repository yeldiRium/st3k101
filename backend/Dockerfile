FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

RUN pip install -r /app/requirements.txt

WORKDIR /app
RUN pybabel compile -d translations

ADD ./nginx/conf.d/nginx.conf /etc/nginx/conf.d/header.conf

ENV FLASK_CONFIG_PATH="/app/flask.cfg"
ENV FLASK_APP="main.py"
