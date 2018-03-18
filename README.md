# EFLA-web survey platform

## About

Seminar work of Hannes Leutloff & Noh Hummel for the computional humanities
seminar @ Goethe University (WS17/18)

### Dependencies:

* docker
* docker-compose
* node
* npm
* pybabel

### Features

- Create numerical surveys
- Completely customize surveys
- Create surveys from templates
- Translate your surveys to almost any language
- Control access to surveys by a modular (and extensible) challenge system
    - Email white- and blacklist
    - Password
    - Agree to terms of service
    - Email verification
- Export survey results to csv
- View result visualizations
- Logging of critical errors via email notification
- Deployment via docker

## Structure of the project

The project is dockerized and contains three different containers:

- db-mongo: A mongodb instance
- memcached: A memcached instance
- websrv-flask: A nginx instance running uswgi and flask

The files for each container can be found in the correspondingly named directory.
Each of those containers is defined in it's own `Dockerfile`.

The whole stack is defined in `docker-compose.yml`. npm dependencies are defined
in `package.json`.

The source code for the application is located at `websrv-flask/app/`.

## Documentation

For learning how to deploy the platform, please read docs/deployment.md.

For learning how to translate the platform, please read docs/translating.md

For information on how to use to object document mapper, please read docs/odm.md

If you want to provide template surveys for your users, please read docs/template_surveys.md

The source code is documented as well.

### Presentation

There will be slides linked.
