FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

RUN pip install -r /app/requirements.txt

ENV FLASK_APP="main.py"
