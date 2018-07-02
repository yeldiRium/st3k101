import json

import requests

from app import app

__author__ = "Noah Hummel"


def validate_captcha(captcha_token):
    # TODO: check captcha here
    return 1
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': app.config['CAPTCHA_SECRET'],
            'response': captcha_token
        }
    )
    data = json.loads(response.text)
    score = data['score'] if data['success'] else 0
    return score >= app.config['CAPTCHA_CONFIDENCE_PERCENTAGE']

