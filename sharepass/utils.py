from flask import render_template
from flask.ext.mail import Message
from sharepass import app, mail
from decorators import async
from smtplib import SMTPException

@async
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException as e:
            # log error
            pass

def send_email(subject, recipients, text_body, html_body):
    sender = '"SharePass" <{}>'.format(app.config['MAIL_USERNAME'])
    msg = Message('[SharePass] '+subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def send_share(recipient, pw):
    send_email(
        subject='New shared password.',
        recipients=[recipient],
        text_body=render_template('email/share.txt', password=pw),
        html_body=render_template('email/share.html', password=pw),
    )

import binascii
import os

def get_token(n=40):
    return binascii.hexlify(os.urandom(n))
