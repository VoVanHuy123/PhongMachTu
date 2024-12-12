from flask import Blueprint, render_template,request,url_for                                                                                                                                                                                                                                                                                                                
from datetime import datetime,date,timedelta
from ..services.medical_services import *

cashier = Blueprint('cashier', __name__, url_prefix='/cashier')

@cashier.route('/', methods=[ 'POST','GET'])
def manager_run():
    medical_info = []
    try:
        page = request.args.get('page', 1, type=int)
        today = datetime.now()
        available_days = [(today + timedelta(days=i)).date() for i in range(-3,7)]

        selected_day = request.form.get('exam_day')

        if not selected_day:
            # Nếu không có ngày được gửi, mặc định là ngày hôm nay
            selected_day = datetime.today().date()
        else:
        # Chuyển đổi chuỗi thành datetime.date
            selected_day = datetime.strptime(selected_day, "%Y-%m-%d").date()
        
        
        medical_exams = get_medical_exams_by_day(selected_day)
        # medical_infos_list = [ get_detail_exam_by_medical_exam_id(med_exam.id) for med_exam in medical_exams]
        medical_infos = [ get_detail_exam_by_medical_exam_id(med_exam.id) for med_exam in medical_exams]
        # medical_infos = medical_infos_list.paginate(page=page, per_page=6, error_out=False)

        
        return render_template('cashier/cashier_page.html',medical_infos=medical_infos,selected_day=selected_day,available_days=available_days)
    except Exception as e:
        print('Error' + str(e))
        return render_template('cashier/cashier_page.html')

@cashier.route('/detail_bill',methods = ['POST'])
def detail_bill():
    medical_exam_id = request.form.get('medical_exam_id')
    medical_exam_info = get_detail_exam_by_medical_exam_id(medical_exam_id)
    total = 0
    for a in medical_exam_info['med_list']:
        total += float(a['price'])
    total_in_word=convert_number_to_words(int(total))
    return render_template('cashier/detail_bill.html',medical_exam_info = medical_exam_info,total=total,total_in_word=total_in_word)

@cashier.route('/pay',methods = ['POST'])
def pay():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'chưa nhận được dữ liệu'}), 400
    
    else:
        try:
            med_exam_id = int(data['medExamId'])
            print(med_exam_id)
            bill = get_bill_by_med_exam_id(med_exam_id)
            bill.is_pay = True
            db.session.commit()
            return jsonify({'success':True,'message' : "Thanh toán thành công","url": url_for('cashier.manager_run')}),200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({'message': str(e)}), 400

