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

### 2.1. Building

### 2.2. Starting

### 2.3 Stopping
