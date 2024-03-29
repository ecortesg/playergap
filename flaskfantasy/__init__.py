import os
import redis
from flask import Flask
from flask_mail import Mail
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG'] = (os.environ.get('DEBUG_VALUE') == 'True')

# Configure database
uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1) #To connect to Heroku Postgres using SQLAlchemy >= 1.4.x
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

# Configure mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('PLAYERGAP_MAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PLAYERGAP_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('PLAYERGAP_MAIL')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail(app)

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
server_session = Session(app)

# Configure reCAPTCHA v2
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE')

from flaskfantasy import routes
