FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN apt update
RUN apt install -y nodejs-legacy
RUN apt install -y npm
RUN npm install --global yarn

COPY ./app /app

RUN pip install -r /app/requirements.txt
RUN yarn install --cwd /app --modules-folder /app/static/vendor