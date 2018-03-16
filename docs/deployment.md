# Deploying EFLA-web

## 0. Setting up for the first time

1. Install dependencies
    1. docker
    2. docker-compose
    4. node
    5. npm
    6. pybabel
2. Configure platform (see 1.)
3. Build containers (see 2.1)
4. Start containers (see 2.2)

## 1. Configuration

### 1.1 flask.cfg

Most of the configurables are located in `EFLA-web/websrv-flask/app/flask.cfg`.

Here are some config values you should change before deploying:

#### Domain Name

Set the `DOMAIN_NAME` field to hostname where the platform will be hosted, for
example: `efla.cs.uni-frankfurt.de`.

If this is set incorrectly, URLs will not be created correctly.

#### SMTP

To send EMails, for example during email verification or for error notifications,
we use SMTP to connect to a mail server. Please provide valid SMTP credentials:

```python
SMTP_FROM_ADDRESS = ""  # the email address used for sending
SMTP_PASSWORD = ""  # the password for the email account
SMTP_SERVER = "smtp.gmx.net"  # the smtp host
SMTP_PORT = 587  # the port to use (587 for TLS)
SMTP_USE_STARTTLS = True  # whether to use TLS encryption
```

#### Error notifications

It is possible to receive notifications when the backend crashes or another
critical bug occurs. Please configure a receiving email address for this:

```python
ERROR_NOTIFICATION_EMAIL_ADDRESS = "someguy@rz.uni-frankfurt.de"
```

#### Tweakables

Some configuration items do not need immediate attention but can be tweaked later:

```python
SHARED_MUTEX_POLLING_TIME = 0.05  # time in seconds between mutex polls

BEL_DEFAULT_LOCALE = "en"  # default language
BABEL_DEFAULT_TIMEZONE = "Europe/Berlin"  # default timezone

STATISTICS_UPDATE_INTERVAL = 1200  # time in seconds between statistics updates
```

### 1.2 Volumes & Backup

With docker, you can mount directories inside of running containers to places
within the host file system. We use volumes to keep the contents of the database
between restarts or rebuilds of the db-mongo container. We use another
volume to place new content into the nginx container without having to rebuild.

The volumes are defined in `EFLA-web/docker-compose.yml`.

#### HowTo: Database backup

Just backup the contents of the `EFLA-web/db-mongo/data` directory as it's mapped
to the data directory of the database container.

Make sure you do this backup as root, as the user id of the container and
the host machine will differ.

We suggest using rsync to copy the database over with permissions intact.

#### HowTo: Applying code changes

When changing code inside the `EFLA-web/websrv-flask/app` directory, you need
to restart the stack to make nginx aware of the changes (see 2.2.).

### 1.2 SSL

The platform comes with a self-signed certificate for testing
purposes that should be replaced before publishing the platform.

To replace it with your own SSL certificate, follow these steps:

1. Obtain a certificate for the DOMAIN_NAME configured in `flask.cfg`.
2. Place the certificate and private key in `EFLA-web/websrv-flask/nginx/ssl`
    1. Private key should be named `private.key`
    2. Certificate should be named `ca_bundle.crt`

To apply your changes, you need to rebuild (described in 2.1)

## 2. Deployment

Run all of these commands from the `EFLA-web` directory.

### 2.1. Building

When building for the first time you need to run:

```bash
cd EFLA-web
npm install
```

To build the containers, then run:

```bash
docker-compose build --no-cache
```
Note: This will not delete the contents of the database.

#### When to build

You need to run `npm install` when:

- JavaScript has been changed
- SCSS files have been changed

Note: It's not necessary to rebuild the containers after `npm install`, just restart the stack.

You need to rebuild when changing:

- Dockerfiles
- SSL certificates
- nginx config

### 2.2. Starting

After building for the first time, you can run:

```bash
docker-compose start
```

To start the services. Use `docker ps` to view running docker services.
To restart, use `docker-compose restart`.

### 2.3 Stopping

To stop the services, run `docker-compose stop`