from app.models import Medicine,MedicineUnit, Category,MedicalExam,DetailExam,ExamRegistration
from config import Config
from app.extensions import db
import hashlib
from sqlalchemy.orm import joinedload
from datetime import datetime

def get_medicine_list():
    return Medicine.query.all()

def get_medicine_categories():
    return Category.query.all()

def get_medicines_by_category_query(category_id):
    return Medicine.query.filter(Medicine.categories.any(Category.id == int(category_id)))

def create_a_medical_exam(diagnosis, exam_day,patient_id,doctor_id):
    return MedicalExam(
            diagnosis=diagnosis,
            exam_day=exam_day,
            patient_id=patient_id,
            doctor_id=doctor_id  
        )

def create_detail_exam(medical_exam_id,medicine_id, instruct,quantity, price):
    return DetailExam(
                medical_exam_id=medical_exam_id,
                medicine_id=medicine_id,
                instruct=instruct,
                quantity=quantity,
                price=price,
            )

def get_exam_registration_by_id(exam_registration_id):
    return ExamRegistration.query.filter_by(id=exam_registration_id).first()

def complete_exam_registration(exam_registration):
    exam_registration.is_watting = False

def process_medicines(medicines, medical_exam_id):
    for med in medicines:
        medicine = Medicine.query.filter_by(name=med['name']).first()
        if not medicine or medicine.inventory < med['quantity']:
            raise ValueError(f"Not enough inventory for {med['name']}.")

        detail_exam = create_detail_exam(
            medical_exam_id=medical_exam_id,
            medicine_id=medicine.id,
            instruct=med['instruct'],
            quantity=med['quantity'],
            price=medicine.unit_price * med['quantity']
        )
        # Update inventory
        medicine.inventory -= med['quantity']
        db.session.add(detail_exam)
