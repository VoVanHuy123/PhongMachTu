# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from flask_migrate import Migrate
from config import Config
from flask_sqlalchemy import SQLAlchemy
from app.admin import init_admin
from config import Config
from app.extensions import db,migrate, login_manager





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    init_admin(app)
    Config.init_cloudinary()

    from .auth.routes import auth
    from .manger.routes import manager
    from .appointment.routes import appointment
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(manager)
    app.register_blueprint(appointment)
    return app
    
