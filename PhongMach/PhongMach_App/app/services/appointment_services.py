from app.models import ExamTime,ExamRegistration, ExamSchedule
from config import Config
from app.extensions import db
import hashlib

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
        is_free=True,
        exam_registration_id=exam_registration_id
    )
    db.session.add(new_exam_scheduled)
    db.session.commit()

def get_exam_scheduled(doctor_id,exam_day):
    return db.session.query(ExamTime).join(ExamSchedule).filter(
        ExamSchedule.doctor_id == doctor_id,
        ExamSchedule.date == exam_day
            ).all()
