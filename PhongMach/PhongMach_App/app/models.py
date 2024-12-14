# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app import db
  
from app.extensions import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Date, DateTime,Time
from datetime import date, time, datetime
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView



class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    create_day = Column(Date, default=date.today)
    active = Column(Boolean, default=True)
    user = relationship("User", backref="account",cascade='all, delete-orphan', uselist=False)  # Thiết lập quan hệ 1-1
    
    def __str__(self):
        return self.user_name


class User(db.Model):
    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    gender = Column(String(50))
    birth_day = Column(Date)
    email = Column(String(50), unique=True, nullable=True)
    image = Column(String(255), nullable=True)
    phone_numbers = relationship('PhoneNumber',backref='user',  cascade='all, delete-orphan', lazy='dynamic')
    
    account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default="user")  
    bill = relationship('Bill',backref='user', cascade='all, delete-orphan', lazy='dynamic')
    # __mapper_args__ = {
    #     'polymorphic_identity': 'user',  
    #     'polymorphic_on': role          
    # }
    

class Doctor(User):
    id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    specialty = Column(String(100), nullable=True) 
    degree = Column(String(100), nullable=True)  
    experience = Column(String(100),nullable=True)
    current_workplace = Column(String(100),nullable=True)
    exam_dates = relationship('ExamSchedule', backref='doctor', lazy=True)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'doctor',  
    # }


class Patient(User):
    id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    insurance_number = Column(String(50), unique=True, nullable=True)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'patient',  
    # }
    


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
    exam_time_id = Column(Integer, ForeignKey('exam_time.id'), nullable=False,primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False,primary_key=True)
    date = Column(Date, nullable=False,primary_key=True)
    is_book = Column(Boolean, nullable=False, default=True)
    exam_registration_id = Column(Integer, ForeignKey('exam_registration.id', ondelete='CASCADE'), nullable=False,unique=True)


class ExamRegistration(db.Model): 
    id = Column(Integer, primary_key=True, )
    symptom = Column(String(255), nullable = True)
    exam_schedule = relationship("ExamSchedule", backref="exam_registration",cascade='all, delete-orphan', uselist=False)
    patient_id = Column(Integer, ForeignKey('patient.id'),nullable = False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'),nullable = False)
    is_waiting = Column(Boolean, default=True)
    doctor = relationship("Doctor", backref="exam_registrations")
    patient = relationship("Patient", backref="exam_registrations") 

class MedicalExam(db.Model):
    id = Column(Integer, primary_key=True)
    diagnosis = Column(String(255))
    exam_day = Column(Date, default=date.today)
    medicines = relationship("DetailExam",cascade='all, delete-orphan',lazy = 'dynamic')
    patient_id = Column(Integer, ForeignKey('patient.id'),nullable = False)
    patient = relationship("Patient", backref="medical_exams")
    doctor_id = Column(Integer, ForeignKey('doctor.id'),nullable = False)
    doctor = relationship("Doctor", backref="medical_exams")
    bill = relationship("Bill", backref="medical_exam", cascade='all, delete-orphan', uselist=False)

class DetailExam(db.Model): 
    medical_exam_id = Column(Integer, ForeignKey('medical_exam.id',ondelete="CASCADE"),primary_key=True, nullable=False)
    medicine_id = db.Column(Integer, ForeignKey('medicine.id'),primary_key=True, nullable=False)
    medicine  = relationship("Medicine", backref="detail_exam",lazy = True)
    unit_id = db.Column(Integer, ForeignKey('unit.id'),nullable=False)
    unit = relationship("Unit", backref="detail_exam",lazy = True)
    instruct = Column(String(255))
    quantity = Column(Float, nullable=False, default = 0)
    price = Column(Float, nullable=False, default = 0)
    

                            

med_category = db.Table(
    "med_category",
    Column("medicine_id", Integer, ForeignKey('medicine.id'), primary_key=True),
    Column("category_id", Integer, ForeignKey('category.id'), primary_key=True)
)


class MedicineUnit(db.Model):
    unit_id = Column(Integer, ForeignKey('unit.id'), primary_key=True, nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicine.id',ondelete="CASCADE"), primary_key=True, nullable=False)
    is_default = Column(Boolean,default = False)
    unit_price = Column(Float, nullable=False, default=0)

    def __str__(self):
        return self.unit.name
    

# Mô hình Category
class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    def __str__(self):
        return self.name
    

# Mô hình Unit
class Unit(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    medicine = relationship("MedicineUnit", backref="unit",lazy = True)
    def __str__(self):
        return self.name
    

# Mô hình Medicine
class Medicine(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    inventory = Column(Float, nullable=False, default=0)
    categories = relationship("Category", secondary=med_category, lazy="subquery", backref=backref('medicine', lazy=True))
    units = relationship("MedicineUnit", backref="medicine", cascade='all, delete-orphan', lazy='dynamic')
    unit_convert = relationship("UnitConvert",backref="medicine",cascade='all, delete-orphan', lazy='dynamic')

    def __str__(self):
        return self.name
    


class UnitConvert(db.Model):
    id = Column(Integer, primary_key=True)
    med_id = Column(Integer, ForeignKey("medicine.id", ondelete="CASCADE"), nullable=False)
    default_unit_id = Column(Integer, ForeignKey("unit.id"))
    target_unit_id = Column(Integer, ForeignKey("unit.id"))
    
    convert_rate = Column(Float, nullable=False, default=1)

class Bill(db.Model):
    id = Column(Integer, primary_key=True)
    exam_fee = Column(Float, nullable=True, default=0)
    is_pay = Column(Boolean, default=False)
    total = Column(Float, nullable=True, default=0)
    medical_exam_id = Column(Integer, ForeignKey("medical_exam.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

class Regulation(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255),unique = True, nullable=False)
    number = Column(Float, nullable=False)
    def __str__(self):
        return self.name
