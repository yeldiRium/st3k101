FROM node:9

# Ugrade to current once https://github.com/npm/npm/issues/19989 is resolved
RUN npm i -g npm@5.6.0

WORKDIR /usr/app
COPY . /usr/app/

RUN npm install

EXPOSE 443
EXPOSE 80
