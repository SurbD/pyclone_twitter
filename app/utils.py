from flask import current_app, render_template
from flask_mail import Message

import jwt
import secrets
from datetime import datetime, timedelta, timezone

from app import mail


def send_email(to, subject, template, **kwargs):
    message = Message(current_app.config['XCLONE_MAIL_SUBJECT_PREFIX'] + subject,
                sender=current_app.config['XCLONE_MAIL_SENDER'], recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)

    mail.send(message)


def get_vcode(expiration=600):
    verification_code = secrets.token_hex(3)

    token = jwt.encode(
        {
            'code': verification_code,
            'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
        },
        current_app.config['SECRET_KEY'],
        algorithm="HS256")

    data = {
        'token': token,
        'vcode': verification_code
    }
    return data


def confirm_vcode(token, vcode):
    try:
        data = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            leeway=timedelta(seconds=10),
            algorithms=["HS256"])
    except:
        return False
    
    if data.get('code') == vcode:
        return True
        
    return False