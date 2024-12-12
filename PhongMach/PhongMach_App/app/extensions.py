from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from twilio.rest import Client
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# twilio_client = Client(
#     Config.TWILIO_ACCOUNT_SID,
#     Config.TWILIO_AUTH_TOKEN
#     )
