# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app import db
  
from app.extensions import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Date, DateTime,Time
from datetime import date, time, datetime
from flask_login import UserMixin



class Account(db.Model, UserMixin):
    id = Column(db.Integer, primary_key=True)
    user_name = Column(db.String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=True)
    create_day = Column(Date, default=date.today)
    active = Column(Boolean, default=True)
    user = relationship("User", backref="account", uselist=False)  # Thiết lập quan hệ 1-1
    
    def __str__(self):
        return self.user_name


class User(db.Model):
    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    gender = Column(String(50))
    birth_day = Column(Date)
    email = Column(String(50), unique=True, nullable=False)
    image = Column(String(255), nullable=True)

    phone_numbers = relationship(
        'PhoneNumber',
        backref='user',
        cascade='all, delete-orphan',  
        lazy=True
    )
    
    account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default="user")  # Thêm trường role
    __mapper_args__ = {
        'polymorphic_identity': 'user',  # Loại mặc định
        'polymorphic_on': role          # Dựa vào `role` để phân biệt vai trò
    }
    

class Doctor(User):
    id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    specialty = Column(String(100), nullable=True) 
    degree = Column(String(100), nullable=True)  
    experience = Column(String(100),nullable=True)
    current_workplace = Column(String(100),nullable=True)
    exam_dates = relationship('ExamSchedule', backref='doctor', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'doctor',  
    }

class Nurse(User):
    id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'nurse',  
    }

class Patient(User):
    id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    insurance_number = Column(String(50), unique=True, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'patient',  
    }
    

class Admin(User):
    id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',  
    }

class PhoneNumber(db.Model):
    id = Column(Integer, primary_key=True)
    number = Column(String(15), nullable=False, unique = True)
    type_number = Column(String(50), nullable=False ,default="personal")
    # user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class ExamTime(db.Model):
    id = Column(Integer, primary_key=True)
    start_time = Column(db.Time, nullable=False)
    end_time = Column(db.Time, nullable=False)
    exam_dates = db.relationship('ExamSchedule', backref='exam_time', lazy = True)

class ExamSchedule(db.Model):
    exam_time_id = Column(Integer, ForeignKey('exam_time.id'), nullable=False, primary_key = True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False, primary_key = True)
    date = Column(Date, nullable=False, primary_key = True)
    is_free = Column(Boolean, nullable=False, default=True)
    exam_registration_id = Column(Integer, ForeignKey('exam_registration.id', ondelete='CASCADE'), nullable = False, unique=True)

class ExamRegistration(db.Model): 
    id = Column(Integer, primary_key=True, )
    symptom = Column(String(255), nullable = True)
    exam_schedule = relationship("ExamSchedule", backref="exam_registration", uselist=False)
    patient_id = Column(Integer, ForeignKey('patient.id'),nullable = False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'),nullable = False)

class MedicalExam(db.Model):
    id = Column(Integer, primary_key=True)
    diagnosis = Column(String(255))
    exam_day = Column(Date, default=date.today)
    medicines = relationship("DetailExam",backref="medical_exam", lazy = True)
    patient_id = Column(Integer, ForeignKey('patient.id'),nullable = False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'),nullable = False)

class DetailExam(db.Model): 
    medical_exam_id = Column(Integer, ForeignKey('medical_exam.id'),primary_key=True, nullable=False)
    medicine_id = db.Column(Integer, ForeignKey('medicine.id'),primary_key=True, nullable=False)
    instruct = Column(String(255))
    quantity = Column(Float, nullable=False, default = 0)
    price = Column(Float, nullable=False, default = 0)
    

                            

med_category = db.Table(
    "med_category",
    Column("medicine_id", Integer, ForeignKey('medicine.id'), primary_key=True),
    Column("category_id", Integer, ForeignKey('category.id'), primary_key=True)
)

med_unit = db.Table(
    "med_unit",
    Column("medicine_id", Integer, ForeignKey('medicine.id'), primary_key=True),
    Column("unit_id", Integer, ForeignKey('medicine_unit.id'), primary_key=True),
)

# Mô hình Category
class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

# Mô hình MedicineUnit
class MedicineUnit(db.Model):
    id = Column(Integer, primary_key=True)
    unit = Column(String(100), nullable=False)

# Mô hình Medicine
class Medicine(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    inventory = Column(Float, nullable=False, default=0)
    unit_price = Column(Float, nullable=False, default=0)
    medical_exams = relationship("DetailExam", backref="medicine", lazy=True)
    categories = relationship("Category", secondary=med_category, lazy="subquery", backref=backref('medicine', lazy=True))
    units = relationship("MedicineUnit", secondary=med_unit, lazy="subquery", backref=backref('medicine', lazy=True))

