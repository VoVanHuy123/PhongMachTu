from flask import Blueprint, render_template, request, redirect,url_for
from app.models import Doctor, ExamTime,ExamSchedule
from ..services.appointment_services import get_exam_time,add_apointment,add_exam_scheduled, get_exam_scheduled, check_existing_schedule
import math
from config import Config
from flask_login import current_user,login_required
from datetime import datetime, timedelta, date
from ..decorators import role_required

appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment.route('/')

def appointment_main():

    if current_user.is_authenticated:

        # Lấy tham số 'page' từ URL, mặc định là 1 nếu không có
        page = int(request.args.get("page", 1))

        # Số lượng phần tử mỗi trang
        page_size = Config.PAGE_SIZE  # lấy từ config nếu có

        # Query dữ liệu
        pagination = Doctor.query.paginate(page=page, per_page=page_size)

        doctors = pagination.items
        total_pages = pagination.pages
        prev_page = pagination.prev_num if pagination.has_prev else 1
        next_page = pagination.next_num if pagination.has_next else total_pages

        return render_template(
            "appointment/doctor_list.html",
            doctors=doctors,
            current_page=page,
            total_pages=total_pages,
            prev_page=prev_page,
            next_page=next_page,
        )
    else:
        return redirect(url_for('auth.user_login'))





# @appointment.route('/book/<int:doctor_id>')
@appointment.route('/book' , methods = ['GET','POST'])
def book():


    doctor_id = request.form.get('doctor_id')
    doctor = Doctor.query.get(doctor_id)

    # Lấy ngày hiện tại nếu không có ngày được chọn

    selected_day = request.form.get('exam_day')

    if not selected_day:
        # Nếu không có ngày được gửi, mặc định là ngày hôm nay
        selected_day = datetime.today().date()
    else:
        # Chuyển đổi chuỗi thành datetime.date
        selected_day = datetime.strptime(selected_day, "%Y-%m-%d").date()

    # Lấy danh sách các ngày khả dụng
    today = datetime.now()
    available_days = [(today + timedelta(days=i)).date() for i in range(7)]

    # Lấy danh sách giờ khám
    exam_times = get_exam_time()

    # Lấy danh sách giờ đã được đặt cho bác sĩ trong ngày được chọn
    booked_times = ExamSchedule.query.filter_by(doctor_id=doctor_id, date=selected_day).all()
    booked_time_ids = [schedule.exam_time_id for schedule in booked_times]
    

    return render_template(
        'appointment/bookappointment.html',
        doctor=doctor,
        exam_times=exam_times,
        available_days=available_days,
        selected_day=selected_day,
        booked_time_ids=booked_time_ids,
    )

@appointment.route('/appoint/', methods=['GET', 'POST'])
@login_required
def appoint_detail():
    doctor_id = request.form.get('doctor_id')
    exam_time_id =request.form.get('exam_time_id')
    exam_day = datetime.strptime(request.form.get('exam_day'),  "%Y-%m-%d")
    doctor = Doctor.query.get(doctor_id)
    exam_time = ExamTime.query.get(exam_time_id)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('auth.user_login'))


    return render_template('appointment/appoint_detail.html',doctor=doctor, exam_time=exam_time,exam_day = exam_day)

@appointment.route('/confirm-appoint/', methods=['GET', 'POST'])
@login_required
def confirm_appoint():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('auth.user_login'))
        else:
            doctor_id = request.form.get('doctor_id')
            exam_time_id =request.form.get('exam_time_id')
            symptom = str(request.form.get('symptom'))
            exam_day = datetime.strptime(request.form.get('exam_day'),  "%Y-%m-%d %H:%M:%S").date()
            if not check_existing_schedule(exam_time_id,doctor_id,exam_day):
                exam_registration = add_apointment(symptom=symptom, doctor_id=doctor_id, patient_id=current_user.user.id)
                add_exam_scheduled(exam_time_id,doctor_id,exam_day, exam_registration.id)
            return redirect(url_for('appointment.appointment_main'))
    