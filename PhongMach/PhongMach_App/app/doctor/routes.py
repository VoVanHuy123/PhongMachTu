from flask import Blueprint, render_template,request,jsonify,redirect,url_for
from ..services.appointment_services import get_exam_chedule_by_doctor_id_and_date
from ..services.user_services import *
from ..services.medical_services import *
from flask_login import login_user, logout_user, current_user,login_required
from ..decorators import role_required
from datetime import datetime,timedelta,date



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



@doctor_user.route('/details' , methods=['GET', 'POST'])
def doctor_detail():
    doctor_id = request.form.get('doctor_id')
    if not doctor_id:
        doctor_id = current_user.user.id
    doctor = get_doctor_by_id(doctor_id)
    return render_template('appointment/doctor_detail.html',doctor=doctor)


@doctor_user.route('/medical', methods=['GET', 'POST'])
def create_medical():

    if request.method == 'POST':
        exam_registration_id = request.form.get('exam_registration_id')
        patient_id = int(request.form.get('patient_id'))
        patient = get_patinent_by_id(patient_id)
        medicine_list = get_medicine_list()
        medicine_categories = get_medicine_categories()
        exam_dayy =  datetime.strptime(request.form.get('exam_dayy'), "%Y-%m-%d").date()
        result = [{
            'id': med.id,
            'name': med.name,
            'unit': med.units[0].unit if med.units else None,  # Lấy đơn vị đầu tiên (nếu có)
            'unit_list': [unit.unit for unit in med.units]
            
        } for med in medicine_list
        ]

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
        print('có')
        medicines = get_medicines_by_category_query(category_id)
    else:
        print('không')
        medicines = Medicine.query

    # Lọc thêm theo từ khóa tìm kiếm
    if query:
        medicines = medicines.filter(Medicine.name.ilike(f"%{query}%"))
    # Trả về kết quả dưới dạng JSON
    result = [{
            'id': med.id,
            'name': med.name,
            'unit': med.units[0].unit if med.units else None,  # Lấy đơn vị đầu tiên (nếu có)
            'unit_list': [unit.unit for unit in med.units]
            
        } for med in medicines
        ]
    return jsonify(result)





@doctor_user.route('/create-medical-exam', methods=['POST'])
def create_medical_exam():
    
    data = request.get_json()
    print(data)
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
        exam_registration = get_exam_registration_by_id(exam_registration_id)
        complete_exam_registration(exam_registration)
        db.session.commit()
        return jsonify({
            "message": "Medical exam created successfully.",
            "redirect_url": url_for('doctor_user.doctor_user_run')  # Trả URL để frontend xử lý
        }), 200

    except Exception as e:
        print (str(e))
        db.session.rollback()
        return jsonify({"message": str(e)}), 400