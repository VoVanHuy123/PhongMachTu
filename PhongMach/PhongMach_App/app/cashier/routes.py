from flask import Blueprint, render_template,request,url_for                                                                                                                                                                                                                                                                                                                
from datetime import datetime,date,timedelta
from ..services.medical_services import *
from ..services.report_services import get_total
from ..services.report_services import *
from calendar import monthrange

cashier = Blueprint('cashier', __name__, url_prefix='/cashier')

@cashier.route('/', methods=[ 'POST','GET'])
def manager_run():
    medical_info = []
    try:
        
        today = datetime.now()
        available_days = [(today + timedelta(days=i)).date() for i in range(-3,7)]

        selected_day = request.form.get('exam_day')
        search_name = request.form.get('search_name') or request.args.get('search_name', '')
        page = request.args.get('page', 1, type=int)
        per_page = 8
        if not selected_day:
            selected_day = request.args.get("selected_day")
            if selected_day:
                selected_day = datetime.strptime(selected_day, "%Y-%m-%d").date()
            else:
                selected_day = today.date()  # Chuyển đổi `today` thành `datetime.date`
        else:
            selected_day = datetime.strptime(selected_day, "%Y-%m-%d").date()
        
        if not search_name:
            search_name = request.args.get("search_name","")
        
        print(search_name)
        print(selected_day)
        # medical_exams = get_medical_exams_by_day(selected_day)
        pagination =get_medical_exam_by_patient_name_and_day(search_name,selected_day).paginate(page=page, per_page=per_page, error_out=False)
        
        medical_exams = pagination.items
        medical_infos = [ get_detail_exam_by_medical_exam_id(med_exam.id) for med_exam in medical_exams]

        
        return render_template('cashier/cashier_page.html',
                               pagination=pagination,
                               medical_infos=medical_infos,
                               selected_day=selected_day,
                               available_days=available_days,
                               search_name=search_name)
    except Exception as e:
        print('Error' + str(e))
        return render_template('cashier/cashier_page.html')

@cashier.route('/detail_bill',methods = ['POST'])
def detail_bill():
    medical_exam_id = request.form.get('medical_exam_id')
    medical_exam_info = get_detail_exam_by_medical_exam_id(medical_exam_id)
    total = get_total(medical_exam_info)
    
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
            medical_exam_info = get_detail_exam_by_medical_exam_id(med_exam_id)
            total = get_total(medical_exam_info)
            bill = get_bill_by_med_exam_id(med_exam_id)
            bill.is_pay = True
            bill.total = total
            db.session.commit()
            return jsonify({'success':True,'message' : "Thanh toán thành công","url": url_for('cashier.manager_run')}),200
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({'message': str(e)}), 400
        


