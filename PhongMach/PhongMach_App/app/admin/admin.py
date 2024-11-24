from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import  User, ExamTime,ExamSchedule,PhoneNumber,Account,Patient,Doctor, ExamRegistration, Medicine, Category

from app.extensions import db

def init_admin(app):
    """
    Hàm khởi tạo Flask-Admin.
    """
    admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(ExamTime, db.session))
    admin.add_view(ModelView(ExamSchedule, db.session))
    admin.add_view(ModelView(PhoneNumber, db.session))
    admin.add_view(ModelView(Account, db.session))
    admin.add_view(ModelView(Patient, db.session))
    admin.add_view(ModelView(Doctor, db.session))
    admin.add_view(ModelView(ExamRegistration, db.session))
    admin.add_view(ModelView(Medicine, db.session))
    admin.add_view(ModelView(Category, db.session))
