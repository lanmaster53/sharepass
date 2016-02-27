from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sharepass.db')
DEBUG = True
TESTING = False
SECRET_KEY = 'development key'
PASSWORD_TTL = 600 # time in seconds
# email server
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
#os.environ.get('NAME')
MAIL_USERNAME = '<mailgun username here>'
MAIL_PASSWORD = '<mailgun password here>'

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)
mail = Mail(app)

def initdb():
    db.create_all()
    print 'Database initialized.'

def dropdb():
    db.drop_all()
    print 'Database dropped.'

import models
import views
