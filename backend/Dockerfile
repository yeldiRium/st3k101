FROM tiangolo/uwsgi-nginx-flask:python3.6

ADD ./nginx/conf.d/nginx.conf /etc/nginx/conf.d/header.conf

WORKDIR /app
ADD ./app/requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY ./app /app
RUN pybabel compile -d translations

ENV FLASK_CONFIG_PATH="/app/flask.cfg"
ENV FLASK_APP="main.py"