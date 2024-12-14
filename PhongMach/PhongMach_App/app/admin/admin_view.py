from flask import request, render_template, redirect, url_for, jsonify, flash
from flask_admin import Admin, expose,BaseView
from flask_admin.contrib.sqla import ModelView
from app.models import   Medicine, Category ,Unit,MedicineUnit,UnitConvert,MedicalExam,DetailExam,ExamRegistration,ExamSchedule,ExamTime,User,Regulation,Bill
from app.extensions import db
from wtforms import SelectField
from flask import request,redirect,render_template
from ..services.medical_services import *
from ..services.user_services import *
from ..services.report_services import *
from datetime import date
from calendar import monthrange,calendar



class MedicineView(ModelView):
    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        if request.method == 'POST':
            # Lấy dữ liệu từ JavaScript thông qua JSON
            data = request.get_json()
            
            try:
                # Tạo thuốc mới
                new_medicine = create_medicine(
                    name=data.get('medicine_name'),
                    inventory=float(data.get('inventory', 0))
                )
                db.session.add(new_medicine)
                db.session.flush()

                # Thêm đơn vị cơ bản
                default_unit_id = data.get('default_unit')
                default_unit_price = data.get('default_unit_price')
                if default_unit_id:
                    default_unit = create_default_medicine_unit(
                        int(default_unit_id),
                        new_medicine.id,
                        float(default_unit_price),
                    )
                    db.session.add(default_unit)
                    db.session.flush()
                else:
                    return jsonify({'message': 'chưa chọn đơn vị cơ bản'})

                # Thêm các đơn vị khác
                for unit in data.get('units', []):
                    unit_id = int(unit['unit_id'])
                    unit_price = float(unit['unit_price'])
                    unit_convert_rate = float(unit['convert_rate'])
                    new_unit = create_medicine_unit(
                        unit_id,
                        new_medicine.id,
                        unit_price=unit_price,
                    )
                    db.session.add(new_unit)
                    db.session.flush()
                    #thêm các quy đổi đơn vị
                    unit_convert = create_unit_convert(new_medicine.id, int(default_unit_id),unit_id,unit_convert_rate)
                    db.session.add(unit_convert)


                # Thêm loại thuốc
                categories = data.get('categories')
                if categories:
                    selected_categories = Category.query.filter(Category.id.in_(categories)).all()
                    new_medicine.categories.extend(selected_categories)
                else:
                    return jsonify({'message': 'chưa chọn categories'})

                db.session.commit()
                return jsonify({
                    'message': 'Thêm thuốc thành công!',
                    'redirect_url': url_for('.index_view')  # URL cho giao diện danh sách
                }), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400

        # Lấy dữ liệu cho form
        units = Unit.query.all()
        categories = Category.query.all()

        return self.render('admin/create_medicine.html', units=units, categories=categories)

    # Ghi đè trang chỉnh sửa thuốc
    # Trang chỉnh sửa thuốc (GET)
    @expose('/edit/<int:id>/', methods=['GET'])
    def edit_view(self, id):
        # Lấy thông tin thuốc theo id
        medicine = get_medicine_by_id(id)
        medicine_units = get_medicine_units_by_med_id(id)
        medicine_units_list = [
            {
                "unit_id": unit.unit_id,
                "unit_price":unit.unit_price,
                "is_default":unit.is_default,
                "covert_rate" : get_unit_convert_rate_by_med_and_unit_id(id,unit.unit_id)
            }
            for unit in medicine_units
        ]
        units = Unit.query.all()  # Lấy tất cả các đơn vị
        categories = Category.query.all()  # Lấy tất cả các loại thuốc
        return self.render('admin/edit_medicine.html', medicine=medicine, units=units, categories=categories,medicine_units_list = medicine_units_list)

    # Xử lý chỉnh sửa thuốc (POST)
    @expose('/edit/<int:id>/', methods=['POST'])
    def edit_medicine(self, id):
        data = request.get_json()
        medicine = Medicine.query.get(id)

        if medicine:
            try:
                # Cập nhật thông tin thuốc
                medicine.name = data.get('medicine_name')
                medicine.inventory = float(data.get('inventory', 0))

                # Cập nhật đơn vị cơ bản
                default_unit_id = data.get('default_unit')
                default_unit_price = data.get('default_unit_price')
                if default_unit_id:
                    #lấy đơn vị có default true của thuốc vì thuốc chỉ có 1 đơn vị cơ bản
                    default_unit = MedicineUnit.query.filter_by(medicine_id=medicine.id, is_default=True).first()
                    if default_unit:
                        default_unit.unit_id = int(default_unit_id)
                        default_unit.unit_price = float(default_unit_price)
                    else:
                        #nếu không thì thêm vào
                        new_default_unit = create_default_medicine_unit(
                            int(default_unit_id),
                            medicine.id,
                            float(default_unit_price),
                        )
                        db.session.add(new_default_unit)
                        db.session.flush()

                update_medicine_units(medicine,data)

                    

                # Cập nhật các loại thuốc
                categories = data.get('categories')
                if categories:
                    selected_categories = Category.query.filter(Category.id.in_(categories)).all()
                    medicine.categories = selected_categories

                db.session.commit()
                return jsonify({
                    'message': 'Cập nhật thuốc thành công!',
                    'redirect_url': url_for('.index_view')  # URL cho giao diện danh sách
                }), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
                
        else:
            return jsonify({'message': 'Không tìm thấy thuốc'}), 404
        
    

    # Xử lý xóa thuốc (POST)
    # @expose('/delete/<int:id>/', methods=['POST'])
    # def delete_medicine(self, id):
    #     medicine = get_medicine_by_id(id)
    #     print(medicine)
    #     if not medicine:
    #         return jsonify({'message': 'Không tìm thấy thuốc'}), 404

    #     try:

    #         # Xóa thuốc và các quan hệ liên quan
    #         db.session.delete(medicine)
    #         db.session.commit()
    #         flash('Xóa thuốc thành công.', 'success')
    #         return jsonify({'message': 'Xóa thành công'}), 200
    #     except Exception as e:
    #         db.session.rollback()
    #         flash(f'Lỗi khi xóa thuốc: {str(e)}', 'danger')
    #         return jsonify({'error': str(e)}), 400

class RegiterView(BaseView):
    @expose('/', methods = ['POST', 'GET'])
    def create_auth(self):
        err_msg = None  

        if request.method == 'POST':
            
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            user_name = request.form.get('user_name')
            password = request.form.get('password')
            
            gender = request.form.get('gender')
            confirm = request.form.get('confirm')
            
            role = request.form.get('role')
            try:
                if password.strip().__eq__(confirm.strip()):
                    add_user(
                            first_name=first_name,
                            last_name=last_name,
                            user_name= user_name,
                            password= password,
                            role=role,
                            gender=gender,
                            )
                    print("đúng")
                    return redirect(url_for('.index_view'))
                else:
                    print("sai")
                    err_msg = "Mật khẩu không khớp"
                    return redirect(url_for('auth.user_login'),err_msg =err_msg)
            except Exception as ex :
                db.session.rollback() 
                err_msg = "Could not add user" + str(ex)
        return self.render('admin/admin_register.html')
    
class ReportView(BaseView):
    @expose('/', methods=['GET'])
    def report(self, **kwargs):  # Thêm **kwargs để nhận các tham số bổ sung
        # Nhận giá trị tháng và năm từ yêu cầu (mặc định là tháng 12 năm 2024)
        current_date = datetime.now()
        month = request.args.get('month', default=current_date.month, type=int)
        year = request.args.get('year', default=current_date.year, type=int)
        category = request.args.get('category', default=1,type=int)

        # Tính tổng số ngày trong tháng đã chọn
        days_in_month = monthrange(year, month)[1]
        patient_counts = [count_patients_in_day(day,month,year) for day in range(1, days_in_month + 1)]
        daily_total_list = [get_daily_revenue(day,month,year) for day in range(1, days_in_month + 1)]
        month_total = 0
        for total in daily_total_list:
            month_total += total 
        # Lấy số bệnh nhân cho từng ngày
        patient_report = {
            "patient_counts" : patient_counts,
            "daily_total_list" : daily_total_list,
            "month_total": month_total,
        }
        
        medicine_sold = count_medicine_by_category(month,year,category)
        categories = get_medicine_categories()
        medicine_report = {
            "medicine_sold" : medicine_sold,
            "categories" : categories
        }
        # Trả về giao diện với dữ liệu
        return self.render('admin/report.html', 
                           days_in_month=days_in_month,
                           patient_report=patient_report,
                           month = month,
                           year=year,
                           category=category,
                           medicine_report=medicine_report)
    
    @expose('/get_revenue_info', methods=['GET'])
    def get_revenue_info(self, **kwargs):
        try:
            current_date = datetime.now()
            month = request.args.get('month', default=12, type=int)
            year = request.args.get('year', default=2024, type=int)

            # Tính toán dữ liệu
            moths_revenue = [get_monthly_revenue(i,year) for i in range(1,13)]
            months = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            return jsonify({
                'months': months,
                'moths_revenue':moths_revenue,
                'message': "oonr",
            })
        except Exception as e:
            return jsonify({
                'error': str(e)
            }), 500

def init_admin(app):
    """
    Hàm khởi tạo Flask-Admin.
    """
    admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")
    admin.add_view(MedicineView(Medicine, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Unit, db.session))
    admin.add_view(ModelView(Regulation, db.session))
    admin.add_view(ModelView(Bill, db.session))
    admin.add_view(ModelView(MedicalExam, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Account, db.session))
    admin.add_view(ModelView(DetailExam, db.session))
    admin.add_view(ModelView(ExamRegistration, db.session))
    admin.add_view(ModelView(ExamSchedule, db.session))
    
    admin.add_view(RegiterView(name='Regiter', endpoint='regiter'))
    admin.add_view(ReportView(name="Report", endpoint='report'))
    


