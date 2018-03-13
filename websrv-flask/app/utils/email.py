import smtplib
from email.mime.text import MIMEText

from flask import g


def send_mail(to: str, subject: str, message: str):

    sender = g._config["SMTP_FROM_ADDRESS"]
    receivers = [to]
    server = g._config["SMTP_SERVER"]
    port = g._config["SMTP_PORT"]

    email = MIMEText(message)
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = to

    smtp = smtplib.SMTP(server, port=port)
    if g._config["SMTP_USE_STARTTLS"]:
        smtp.starttls()
    smtp.login(g._config["SMTP_FROM_ADDRESS"], g._config["SMTP_PASSWORD"])
    smtp.sendmail(sender, receivers, email.as_string())
