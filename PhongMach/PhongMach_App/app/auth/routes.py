from flask import Blueprint, render_template,request,redirect, url_for,jsonify
from ..services.user_services import add_user_default,check_login, get_user_account_by_id
from ..services.appointment_services import *
from app.extensions import db, login_manager
from datetime import datetime
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import *

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    err_msg = None
    if request.method.__eq__("POST"):
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        user_account = check_login(user_name=user_name, password=password)

        if user_account and user_account.user.role == 'patient':
            login_user(user_account)#ghi nhận biến toàn cục user
            return redirect(url_for('main.index'))
        else:
            if user_account and user_account.user.role == 'doctor':
                login_user(user_account)#ghi nhận biến toàn cục user
                return redirect(url_for('doctor_user.doctor_user_run'))
            else:
                err_msg = "username or password is incorrcet"
    return render_template('auth/login.html',err_msg = err_msg)


# tự gọi khi đăng nhập thành công
@login_manager.user_loader
def user_load(user_id):
    return get_user_account_by_id(user_id)

@auth.route('/logout')
def user_logout():
    logout_user()
    return redirect(url_for('auth.user_login'))

@auth.route('/register',  methods=['GET', 'POST'])
def user_register():

    err_msg = None  

    if request.method == 'POST':
        
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        birth_day = request.form.get('birth_day')
        gender = request.form.get('gender')
        confirm = request.form.get('confirm')
        image_path = None
        insurance_number = request.form.get('insurance_number')
        try:
            if password.strip().__eq__(confirm.strip()):
                image = request.files.get('image')
                if image:
                    res = cloudinary.uploader.upload(image)
                    image_path = res['secure_url']
                add_user_default(first_name=first_name,
                        last_name=last_name,
                        user_name= user_name,
                        password= password,
                        email=email,
                        phone_number=phone_number,
                        gender=gender,
                        birth_day=datetime.strptime(birth_day, '%Y-%m-%d').date(),
                        image = image_path,
                        insurance_number = insurance_number
                        )
                return redirect(url_for('auth.user_login'))
            else:
                err_msg = "Mật khẩu không khớp"
                return redirect(url_for('auth.user_login'))
        except Exception as ex :
            db.session.rollback() 
            err_msg = "Could not add user" + str(ex)
        
    return render_template('auth/register.html', err_msg = err_msg)

@auth.route('/user_page')

def user_page():
    page = request.args.get('page', 1, type=int)  # Lấy trang hiện tại từ URL (mặc định là trang 1)
    per_page = 5  
    pagination = get_exam_registration_paginate_by_patient_id(current_user.user.id, page, per_page)

    # Lấy dữ liệu phân trang
    exam_registrations = [{
        "id": exam_regis.id,
        "doctor_name": exam_regis.doctor.first_name + " " + exam_regis.doctor.last_name,
        "start_time": exam_regis.exam_schedule.exam_time.start_time.strftime('%H:%M'),
        "end_time": exam_regis.exam_schedule.exam_time.end_time.strftime('%H:%M'),
        "watting_status": exam_regis.is_waiting,
        "day": exam_regis.exam_schedule.date.strftime('%d-%m-%Y'),
        "symptom": exam_regis.symptom,
    } for exam_regis in pagination.items]  # .items chứa các đối tượng trong trang hiện tại

    return render_template('auth/user_page.html',exam_registrations=exam_registrations,pagination=pagination)