from app.models import Doctor,User, PhoneNumber, Account, Patient
from config import Config
from app.extensions import db
import hashlib
from datetime import datetime
from flask import jsonify

def count_Doctor():
    return Doctor.query.count()

def get_doctors(page=1):

    page_size = Config["PAGE_SIZE"]
    start = (page - 1) * page_size
    doctors = Doctor.query.slice(start, start + page_size)
    return doctors

def get_doctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)

def get_patinent_by_id(user_id):
    return Patient.query.filter_by(id=user_id).first()
def add_user_default(first_name, last_name, user_name, password, email, phone_number, gender, birth_day, **kwargs):
    password = str(hashlib.md5((password).strip().encode('utf-8')).hexdigest())
    insurance_number = str(kwargs.get('insurance_number'))
    
    account = Account(
        user_name=user_name,
        password=password,
    )
    db.session.add(account)
    db.session.commit()
    
    patient = Patient(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_day=birth_day,
            email=email,
            image = kwargs.get('image'),
            account_id = account.id,
            role = 'patient',
            insurance_number = insurance_number,
      
        )
    db.session.add(patient)
    db.session.commit()

    phone = PhoneNumber(
        number=phone_number,
        user_id = patient.id,
    )
    db.session.add(phone)
    db.session.commit()

def check_login(user_name, password):
    if user_name and password:
        password = str(hashlib.md5((password).strip().encode('utf-8')).hexdigest())

        return Account.query.filter(Account.user_name.__eq__(user_name.strip()),
                                Account.password.__eq__(password)).first()

def get_user_account_by_id(user_id):
    return Account.query.get(user_id)

def update_user_info(account,data):
    account.user.first_name = data['first_name']
    account.user.last_name = data['last_name']
    account.user.email = data['email']
    account.user.gender = data['gender']
    account.user.birth_day = datetime.strptime(data['birth_day'], '%Y-%m-%d').date()
    
def get_user_form_data(request):
    """
    Lấy dữ liệu người dùng từ request form và file upload.
    """
    form_data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'phone_number': request.form.get('phone_number'),
        'gender': request.form.get('gender'),
        'birth_day': request.form.get('birth_day'),
        'image': request.files.get('image'),
        'insurance_number': request.form.get('insurance_number'),
        'confirm': request.form.get('confirm'),
    }
    return form_data

def get_user_account_form_data(request):
    form_data = {
        'user_name': request.form.get('user_name'),
        'password': request.form.get('password'),
    }
    return form_data

