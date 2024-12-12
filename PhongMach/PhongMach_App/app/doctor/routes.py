from flask import Blueprint, render_template,request,jsonify,redirect,url_for
from ..services.appointment_services import get_exam_chedule_by_doctor_id_and_date
from ..services.user_services import *
from ..services.medical_services import *
from flask_login import login_user, logout_user, current_user,login_required
from ..decorators import role_required
from datetime import datetime,timedelta,date
import cloudinary.uploader



doctor_user = Blueprint('doctor_user', __name__, url_prefix='/doctor_user')

@doctor_user.route('/',methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_user_run():
    
    today = datetime.now()
    available_days = [(today + timedelta(days=i)).date() for i in range(7)]

    selected_day = request.form.get('exam_day')

    if not selected_day:
        # Nếu không có ngày được gửi, mặc định là ngày hôm nay
        selected_day = datetime.today().date()
    else:
        # Chuyển đổi chuỗi thành datetime.date
        selected_day = datetime.strptime(selected_day, "%Y-%m-%d").date()
    
    exam_schedules = get_exam_chedule_by_doctor_id_and_date(current_user.user.id , selected_day)

    return render_template('doctor/doctor_page.html', exam_schedules=exam_schedules,available_days= available_days,selected_day=selected_day)


@doctor_user.route('/edit_doctor_info' , methods=['GET', 'POST'])
def edit_doctor_info():
    if request.method == 'POST':
        doctor_info = get_user_form_data(request)
        doctor_account_info = get_user_account_form_data(request)
        try:
            data = get_user_form_data(request)
            update_doctor_user_info(current_user.user, data)
            
            if data['phone_number'] != None: 
                if not current_user.user.phone_numbers.all():
                    phone_number = PhoneNumber(number = data['phone_number'])
                    phone_number.user_id = current_user.user.id
                    db.session.add(phone_number)
                else:
                    current_user.user.phone_numbers[0].number = data['phone_number']
            if data['image']:
                try:
                    res = cloudinary.uploader.upload(data['image'])
                    image_path = res['secure_url']
                    current_user.user.image = image_path
                except Exception as e:
                    return jsonify({'success': False, 'message': f'Upload ảnh thất bại: {str(e)}'}), 500
            db.session.commit()
            return jsonify({'success': True}),200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

@doctor_user.route('/details' , methods=['GET', 'POST'])
def doctor_detail():
    
    if current_user.user.role == 'doctor':
        doctor_id = request.form.get('doctor_id')
        phone_number = ""
        phone_numbers = current_user.user.phone_numbers.all()  # .all() lấy kết quả từ truy vấn
        if phone_numbers:
            phone_number = phone_numbers[0].number
        if not doctor_id:
            doctor_id = current_user.user.id
        doctor = get_doctor_by_id(doctor_id)
        return render_template('doctor/doctor_detail.html',doctor=doctor,phone_number=phone_number)
    if current_user.user.role == 'patient':
        doctor_id = request.form.get('doctor_id')
        
        doctor = get_doctor_by_id(doctor_id)
        phone_number = ""
        phone_numbers = doctor.phone_numbers.all()
        if phone_numbers:
            phone_number = phone_numbers[0].number
        return render_template('doctor/doctor_detail.html',doctor=doctor,phone_number=phone_number)
    else:
        # Xử lý nếu role không phải 'doctor' hoặc 'patient'
        return "Unauthorized access", 403


@doctor_user.route('/medical', methods=['GET', 'POST'])
def create_medical():

    if request.method == 'POST':
        exam_registration_id = request.form.get('exam_registration_id')
        patient_id = int(request.form.get('patient_id'))
        patient = get_patinent_by_id(patient_id)
        medicine_list = get_medicine_list()
        medicine_categories = get_medicine_categories()
        exam_dayy =  datetime.strptime(request.form.get('exam_dayy'), "%Y-%m-%d").date()
        result = get_medicine_info(medicine_list)

    return render_template('doctor/medical.html',
                           patient = patient,
                           medicine_list = result,
                           medicine_categories = medicine_categories,
                           exam_dayy = exam_dayy,
                           exam_registration_id = exam_registration_id,
                           )





@doctor_user.route('/search_medicine', methods=['GET'])
def search_medicine():
    query = request.args.get('query', '').strip().lower()
    category_id = request.args.get('category', '')

    
    # Lọc thuốc theo danh mục nếu được chọn
    if category_id:
        medicines = get_medicines_by_category_query(category_id)
    else:
        medicines = Medicine.query
        

    # Lọc thêm theo từ khóa tìm kiếm
    if query:
        medicines = medicines.filter(Medicine.name.ilike(f"%{query}%"))
        # for med in medicines:
            # print(unit.name for unit in get_unit_list_by_medicine_id(med.id))
    # Trả về kết quả dưới dạng JSON
    result = get_medicine_info(medicines)
    
    return jsonify(result)

@doctor_user.route('/add_medicine', methods=['POST'])
def add_medicine():
    try:
        data = request.json
        medicine_id = data['medicine_id']
        unit_id = data['unit_id']
        quantity = data['quantity']
        #lấy thuốc
        medicine = get_medicine_by_id(medicine_id)
        #lấy danh sách đơn vị của thuốc đó
        med_unit_list = get_unit_list_by_medicine_id(medicine_id)
        list_unit = [{
            'id': unit.id,
            'name': unit.name,
        }for unit in med_unit_list]
        for unit in list_unit:
            print(unit['id'], unit['name'])
        #lấy quy đổi của unit_id này
        convert_rate = get_unit_convert_rate_by_med_and_unit_id(medicine_id,unit_id)
        if not medicine:
            raise ValueError(f"Không tìm thấy thuốc với ID: {medicine_id}")
        if not list_unit:
            raise ValueError(f"Không có unit_list")
        convert_rate = get_unit_convert_rate_by_med_and_unit_id(medicine_id, unit_id)
        if not convert_rate:
            raise ValueError(f"Không tìm thấy tỷ lệ chuyển đổi cho thuốc ID {medicine_id} và đơn vị ID {unit_id}")

       #kiểm tra có đủ trong inventory của thuốc không
        is_enough_inventory(medicine, quantity, convert_rate)

        return jsonify({
            "success": True, 
            "list_unit": list_unit,
            "message": "Thuốc đã được thêm thành công!"}),200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@doctor_user.route('/create-medical-exam', methods=['POST'])
def create_medical_exam():
    
    data = request.get_json()
    if not data:
            return jsonify({"message": "Invalid JSON format."}), 400
    diagnosis = data.get('diagnosis')
    exam_day = datetime.strptime(data.get('examDate'), '%d/%m/%Y').date()
    patient_id = int(data.get('patientId'))
    exam_registration_id = int(data.get('examRegistrationId'))
    #kiểm tra dữ liệu lấy từ frontend
    if not diagnosis:
        return jsonify({"message": "Diagnosis is required."}), 400
    if not exam_day or not isinstance(exam_day, date):
        return jsonify({"message": "Invalid exam day."}), 400
    if not isinstance(patient_id, int):
        return jsonify({"message": "Invalid patient ID."}), 400
    if not isinstance(exam_registration_id, int):
        return jsonify({"message": "Invalid exam registration ID."}), 400
    

    medicines = data.get('medicines', [])
    if not medicines or len(medicines) == 0:
        return jsonify({"message": "Please add at least one medicine."}), 400  
    print(exam_registration_id)
    try:
        
        medical_exam = create_a_medical_exam(
            diagnosis = diagnosis,
            exam_day = exam_day,
            patient_id = patient_id,
            doctor_id = current_user.user.id,
            )
        
        db.session.add(medical_exam)
        db.session.flush()  # Lấy ID của medical_exam ngay lập tức

        
        process_medicines(medicines, medical_exam.id)

        # cập nhật hoàn thanh đơn đăng kí
        bill = create_bill(medical_exam.id, patient_id)
        db.session.add(bill)
        complete_exam_registration(exam_registration_id)
        db.session.commit()
        return jsonify({
            "message": "Medical exam created successfully.",
            "redirect_url": url_for('doctor_user.doctor_user_run')  # Trả URL để frontend xử lý
        }), 200

    except Exception as e:
        print (str(e))
        db.session.rollback()
        return jsonify({"message": str(e)}), 400