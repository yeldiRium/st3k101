FROM blobfish42/uwsgi-nginx-flask-celery

COPY ./app /app

RUN pip install -r /app/requirements.txt

ENV FLASK_APP="main.py"
ENV FLASK_CONFIG_PATH="flask.cfg"
ENV CELERY_OBJECT=main.celery