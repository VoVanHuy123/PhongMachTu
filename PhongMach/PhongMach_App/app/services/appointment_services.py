from app.models import ExamTime,ExamRegistration, ExamSchedule, Patient,PhoneNumber,User
from config import Config
from app.extensions import db
import hashlib
from sqlalchemy.orm import joinedload
from datetime import datetime

def get_exam_time():
    return ExamTime.query.all()

def add_apointment(symptom, doctor_id, patient_id):
    new_exam_registration = ExamRegistration(
        symptom=symptom,
        doctor_id=doctor_id,
        patient_id=patient_id,
    )
    db.session.add(new_exam_registration)
    db.session.commit()
    return new_exam_registration

def add_exam_scheduled(exam_time_id,doctor_id,date, exam_registration_id):
   
    new_exam_scheduled = ExamSchedule(
        exam_time_id=exam_time_id,
        doctor_id=doctor_id,
        date=date,
        is_book=True,
        exam_registration_id=exam_registration_id
    )
    db.session.add(new_exam_scheduled)
    db.session.commit()
def check_existing_schedule(exam_time_id,doctor_id,date):
    existing_schedule = db.session.query(ExamSchedule).filter_by(exam_time_id=exam_time_id, doctor_id=doctor_id, date=date).first()
    if existing_schedule:
        return True
    else:
        return False

def get_exam_scheduled(doctor_id,exam_day):
    return db.session.query(ExamTime).join(ExamSchedule).filter(
        ExamSchedule.doctor_id == doctor_id,
        ExamSchedule.date == exam_day
            ).all()

def get_exam_chedule_by_doctor_id_and_date(doctor_id, target_date = datetime.now().date()): #,target_date = datetime.now().date()
    
    results = (
        db.session.query(
            ExamRegistration.is_waiting,
            ExamRegistration.doctor_id,
            ExamRegistration.symptom,            
            ExamSchedule.date,
            ExamTime.end_time,
            ExamTime.start_time,
            Patient.id.label("patient_id"),  
            Patient.first_name,
            Patient.last_name,
            Patient.gender,
            Patient.birth_day,
            Patient.email,
            Patient.image,
            PhoneNumber.number,
            ExamRegistration.id.label("exam_registration_id"),
            ExamRegistration.is_waiting,

        )
        .join(ExamSchedule, ExamRegistration.id == ExamSchedule.exam_registration_id)  # Join với ExamSchedule
        .join(ExamTime, ExamSchedule.exam_time_id == ExamTime.id)
        .join(Patient, ExamRegistration.patient_id == Patient.id)
        .join(PhoneNumber, PhoneNumber.user_id == User.id)
        .filter(
            ExamSchedule.doctor_id == doctor_id,  # Lọc theo doctor_id
            ExamSchedule.date == target_date      # Lọc theo ngày
        )
        .all()
    )
    
    return results

def get_exam_registration_by_patient_id(patient_id):
    return db.session.query(ExamRegistration).filter_by(patient_id=patient_id).all()

def get_exam_registration_paginate_by_patient_id(patient_id, page=1, per_page=10):
    return ExamRegistration.query.filter_by(patient_id=patient_id)\
        .paginate(page=page, per_page=per_page, error_out=False)