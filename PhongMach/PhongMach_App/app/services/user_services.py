from app.models import Doctor,User, PhoneNumber, Account, Patient
from config import Config
from app.extensions import db
import hashlib

def count_Doctor():
    return Doctor.query.count()

def get_doctors(page=1):

    page_size = Config["PAGE_SIZE"]
    start = (page - 1) * page_size
    doctors = Doctor.query.slice(start, start + page_size)
    return doctors

def add_user_default(first_name, last_name, user_name, password, email, phone_number, gender, birth_day, **kwargs):
    password = str(hashlib.md5((password).strip().encode('utf-8')).hexdigest())
    
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
            role = 'patient'
      
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

def get_user_by_id(user_id):
    return Account.query.get(user_id)
