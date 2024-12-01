from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import  User, ExamTime,ExamSchedule,PhoneNumber,Account,DetailExam,Doctor, ExamRegistration, Medicine, Category ,MedicineUnit,MedicalExam
from app.extensions import db
from flask_admin.form import rules
from flask_wtf import FlaskForm
from wtforms import SelectField



# class MyUserView(ModelView):
#     column_list = ['id', ' last_name', 'first_name', 'gender', 'birth_day', 'email', 'phone_numbers','role']
#     column_searchable_list = ['birth_day']
#     column_editable_list = ['last_name', 'first_name', 'role']
#     can_export = True
#     column_filters = ['role']
#     column_labels = {
#         'id': 'ID',
#         'last_name': 'last_name',
#         'first_name': 'first_name',
#         'phone_numbers': 'SĐT',
#         'gender': 'gender',
#         'email': 'Email',
#         'birth_day': 'address',
#         'role': 'role',
#     }
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
    admin.add_view(ModelView(ExamRegistration, db.session))
    admin.add_view(ModelView(Medicine, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Doctor, db.session))
    admin.add_view(ModelView(MedicalExam, db.session))
    admin.add_view(ModelView(DetailExam, db.session))
