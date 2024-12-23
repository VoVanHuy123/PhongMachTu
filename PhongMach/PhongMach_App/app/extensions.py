from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from twilio.rest import Client
from config import Config
from flask_mail import Mail
# from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
# celery = Celery(__name__, broker=Config.MAIL_PASSWORD , backend=Config.CELERY_RESULT_BACKEND )
# twilio_client = Client(
#     Config.TWILIO_ACCOUNT_SID,
#     Config.TWILIO_AUTH_TOKEN
#     )
