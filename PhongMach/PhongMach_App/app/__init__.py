# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from config import Config
from app.admin import init_admin
from config import Config
from app.extensions import db,migrate, login_manager, mail 
from app.models import *






def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    init_admin(app)
    Config.init_cloudinary()
    # celery.conf.update(app.config)

    from .auth.routes import auth
    from .cashier.routes import cashier
    from .appointment.routes import appointment
    from .doctor.routes import doctor_user
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(cashier)
    app.register_blueprint(appointment)
    app.register_blueprint(doctor_user)
    return app 
    
