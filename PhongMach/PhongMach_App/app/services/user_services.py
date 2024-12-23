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
    try:
        account = Account(
            user_name=user_name,
            password=password,
        )
        db.session.add(account)
        db.session.flush()
        
        patient = Patient(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_day=birth_day,
                email=email,
                image = kwargs.get('image'),
                account_id = account.id,
                role = 'patient',
                role_mapper = 'patient',
                insurance_number = insurance_number,
        
            )
        db.session.add(patient)
        db.session.flush()

        phone = PhoneNumber(
            number=phone_number,
            user_id = patient.id,
        )
        db.session.add(phone)
        db.session.commit()
    except:
        db.session.rollback()

def add_user(first_name, last_name, user_name,password,role, gender,**kwargs):
    password = str(hashlib.md5((password).strip().encode('utf-8')).hexdigest())
    try:
        user_account = Account(user_name = user_name, password = password)
        db.session.add(user_account)
        db.session.flush()
        user = User(
            first_name = first_name, 
            last_name=last_name,
            role = role,
            account_id = user_account.id,
            gender = gender,
            image = kwargs.get('image'),
            birth_day = kwargs.get('birth_day'),
            )
        db.session.add(user)
        db.session.flush()
        if kwargs.get('phone_number'):
            phone = PhoneNumber(
                number=kwargs.get('phone_number'),
                user_id = user.id,
            )
            db.session.add(phone)
            db.session.flush()
       
        if role == 'doctor':
            user.role_mapper = "doctor"
            doctor = Doctor(id = user.id)
            
            db.session.add(doctor)
            db.session.flush()
       
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(str(e))
def check_login(user_name, password):
    if user_name and password:
        password = str(hashlib.md5((password).strip().encode('utf-8')).hexdigest())

        return Account.query.filter(Account.user_name.__eq__(user_name.strip()),
                                Account.password.__eq__(password)).first()

def get_user_account_by_id(user_id):
    return Account.query.get(user_id)

def update_user_info(user,data):
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.gender = data['gender']
    if data['birth_day']:
        user.birth_day = datetime.strptime(data['birth_day'], '%Y-%m-%d').date()
    else:
        user.birth_day = None

def update_doctor_user_info(user, data):
    try:
        user.specialty = data.get('specialty', user.specialty)
        user.degree = data.get('degree', user.degree)
        user.experience = data.get('experience', user.experience)
        user.current_workplace = data.get('current_workplace', user.current_workplace)
        # Lưu thay đổi
        db.session.commit()
    except:
        db.session.rollback()
    
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
        'specialty' : request.form.get('specialty'),
        'degree' :   request.form.get('degree'),
        'experience' :   request.form.get('experience'),
        'current_workplace' :   request.form.get('current_workplace'),
         
        
    }
    return form_data

def get_user_account_form_data(request):
    form_data = {
        'user_name': request.form.get('user_name'),
        'password': request.form.get('password'),
        'new_password': request.form.get('new_password'),
        'confirm_new_password': request.form.get('confirm_new_password'),
    }
    return form_data


def update_user_account(account,data):
    password = str(hashlib.md5((data['new_password']).strip().encode('utf-8')).hexdigest())
    try:
        account.user_name = data['user_name'],
        account.password = password,
        db.session.commit()
    except:
        db.session.rollback()

