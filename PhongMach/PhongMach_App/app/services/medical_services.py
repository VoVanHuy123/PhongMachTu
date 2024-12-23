from app.models import Medicine,MedicineUnit, Category,MedicalExam,DetailExam,ExamRegistration,Unit,UnitConvert,Bill,Regulation,Patient,ExamSchedule
from config import Config
from app.extensions import db
import hashlib
from sqlalchemy.orm import joinedload
from datetime import datetime
from flask import jsonify
from sqlalchemy.sql.expression import func

def get_medicine_list():
    return Medicine.query.all()

def get_medicine_categories():
    return Category.query.all()

def get_medicines_by_category_query(category_id):
    return Medicine.query.filter(Medicine.categories.any(Category.id == int(category_id)))

def get_num_category():
    return  Category.query.count()
def get_num_unit():
    return Unit.query.count()
def get_num_category_regulation():
    regulation = Regulation.query.filter(Regulation.name == "Loại thuốc").first()
    return regulation.number
def get_num_unit_regulation():
    regulation = Regulation.query.filter(Regulation.name == "Loại đơn vị").first()
    return regulation.number
def get_exam_fee():
    exam_fee =  Regulation.query.filter_by(name = "Phí Khám").first()
    return exam_fee.number
def get_num_patient_in_day():
    num_patient = Regulation.query.filter_by(name = "Số Lượng Bệnh Nhân").first()
    return num_patient.number
def get_exam_regis_in_day(day):
    # Đảm bảo rằng ngày truyền vào đúng định dạng (datetime.date hoặc datetime)
    return db.session.query(func.count(ExamRegistration.id)) \
        .join(ExamRegistration.exam_schedule) \
        .filter(ExamSchedule.date == day) \
        .scalar()
def create_a_medical_exam(diagnosis, exam_day,patient_id,doctor_id):
    return MedicalExam(
            diagnosis=diagnosis,
            exam_day=exam_day,
            patient_id=patient_id,
            doctor_id=doctor_id  
        )
def create_bill(medical_exam_id,patient_id):
    exam_fee  = get_exam_fee()
    return Bill(
        medical_exam_id=medical_exam_id,
        patient_id = patient_id,
        exam_fee = exam_fee
    )
 
def create_detail_exam(medical_exam_id,medicine_id, instruct,quantity, price,unit_id ):
    return DetailExam(
                medical_exam_id=medical_exam_id,
                medicine_id=medicine_id,
                instruct=instruct,
                quantity=quantity,
                price=price,
                unit_id=unit_id ,
            )

def get_exam_registration_by_id(exam_registration_id):
    return ExamRegistration.query.filter_by(id=exam_registration_id).first()

def complete_exam_registration(exam_registration_id):
    exam_registration = get_exam_registration_by_id(exam_registration_id)
    if not exam_registration:
        raise ValueError(f"ExamRegistration with ID {exam_registration_id} not found.")
    exam_registration.is_waiting = False
    db.session.commit()

def get_medicine_by_id(medicine_id):
    return Medicine.query.filter_by(id=medicine_id).first()
def get_unit_by_id(unit_id):
    return Unit.query.filter_by(id=unit_id).first()

def get_medicice_unit_by_med_and_unit_id(med_id, unit_id):
    return MedicineUnit.query.filter_by(medicine_id=med_id, unit_id=unit_id).first()

def get_unit_convert_rate_by_med_and_unit_id(med_id, unit_id):
    unit_convert = UnitConvert.query.filter_by(med_id=med_id, target_unit_id=unit_id).first()
    if unit_convert:
        return unit_convert.convert_rate
    return 1

def is_enough_inventory(medicine, quantity, convert_rate = 1):
    if medicine.inventory < quantity*convert_rate:
        raise ValueError(f"Số lượng thuốc {medicine.name} vượt quá số lượng tồn kho.")
        return False
    else:
        return True
    

def update_inventory(medicine, unit_id, quantity):
    convert_units = get_unit_convert_list_by_medicine_id(medicine.id)
    med_unit = get_medicice_unit_by_med_and_unit_id(medicine.id, unit_id)
    if med_unit.is_default:
        if is_enough_inventory(medicine , quantity):
            medicine.inventory -= quantity
    else:
        for convert in convert_units:
            if unit_id == convert.target_unit_id:
                if is_enough_inventory(medicine , quantity, convert.convert_rate): 
                    medicine.inventory -= (quantity*convert.convert_rate)
                    db.session.commit()
                
            

    
def process_medicines(medicines, medical_exam_id):
    for med in medicines:
        med_unit = get_medicice_unit_by_med_and_unit_id(med['med_id'],med['selected_unit_id'])
        medicine = get_medicine_by_id(med['med_id'])
        update_inventory(medicine, med['selected_unit_id'],med['quantity'])

        detail_exam = create_detail_exam(
            medical_exam_id=medical_exam_id,
            medicine_id=medicine.id,
            instruct=med['instruct'],
            quantity=med['quantity'],
            price = med_unit.unit_price*med['quantity'],
            unit_id = med['selected_unit_id'],
        )
        # Update inventory
        
        db.session.add(detail_exam)
        db.session.commit()


def get_default_unit_of_medicine(medicine_id):
    default_unit = db.session.query(MedicineUnit).filter_by(medicine_id=medicine_id, is_default=True).first()
    if default_unit:
        return db.session.query(Unit).filter_by(id=default_unit.unit_id).first()
    return None

def get_unit_price_by_med_id_and_unit_id(medicine_id, unit_id):
    med_unit = MedicineUnit.query.filter_by(medicine_id=medicine_id,unit_id=unit_id).first()
    return med_unit.unit_price

#hàm lấy tất cả các đơn vị của 1 thuốc
def get_unit_list_by_medicine_id(medicine_id):
    medicine_units = db.session.query(MedicineUnit).filter_by(medicine_id=medicine_id).all()
    units = []
    for medicine_unit in medicine_units:
        unit = db.session.query(Unit).filter_by(id=medicine_unit.unit_id).first()
        if unit:
            units.append(unit)
        
    return units

#hàm lấy thông tin của 1 list thuốc bao gồm cả đơn vị của thuốc và trả về 1 list
def get_medicine_info(medicines):
    results =[
        {
            'id': med.id,
            'name': med.name,
            'unit_default': {
                            'id': get_default_unit_of_medicine(med.id).id,
                            'name': get_default_unit_of_medicine(med.id).name,
                        },
            'inventory': med.inventory,
            'unit_list' : [{
                            "unit_name": unit.name,
                            "unit_id": unit.id,
                        } for unit in get_unit_list_by_medicine_id(med.id)],
            'unit_convert_list': [{
                                    "convert_rate": convert_rate.convert_rate,
                                    "target_unit_id": convert_rate.target_unit_id,
                                } for convert_rate in get_unit_convert_list_by_medicine_id(med.id)],
        } for med in medicines]
        
    return results
#hàm lấy các quy đổi đơn vị của 1 thuốc
def get_unit_convert_list_by_medicine_id(medicine_id):
    return UnitConvert.query.filter_by(med_id = medicine_id).all()
#Hàm lấy danh sách unit 
def get_units():
    return Unit.query.all()

def get_medical_exams_by_patient_id(patient_id):
    return MedicalExam.query.filter_by(patient_id=patient_id)\
        .order_by(MedicalExam.exam_day.desc())

def get_medical_exam_by_id(id):
    return MedicalExam.query.filter_by(id=id).first()

def get_medical_exam_by_patient_name_and_day(search_name, selected_day):
    query = db.session.query(MedicalExam).join(Patient).filter(
        MedicalExam.exam_day == selected_day,
        func.concat(Patient.first_name, " ", Patient.last_name).ilike(f"%{search_name}%")
    )
    return query

def get_medical_exams_by_day(day):
    return MedicalExam.query.filter_by(exam_day=day).all()
def get_detail_exam_by_medical_exam_id(medical_exam_id):
    med_exam = get_medical_exam_by_id(medical_exam_id)
    return {
            "id" : med_exam.id,
            "patient_name": med_exam.patient.first_name + ' ' + med_exam.patient.last_name,
            "patient_gender": med_exam.patient.gender,
            "patient_birthday": med_exam.patient.birth_day,
            "doctor_name": med_exam.doctor.first_name + ' ' + med_exam.doctor.last_name,
            "diagnosis": med_exam.diagnosis,
            "exam_day": med_exam.exam_day,
            "is_pay" : med_exam.bill.is_pay,
            "med_list":[{
                "name" : med.medicine.name,
                "unit" : med.unit.name,
                "quantity": med.quantity,
                "instruct" : med.instruct,
                "unit_price":get_unit_price_by_med_id_and_unit_id(med.medicine.id,med.unit.id),
                "price": med.quantity * get_unit_price_by_med_id_and_unit_id(med.medicine.id,med.unit.id),
            }for med in med_exam.medicines],
        }
def create_medicine(name, inventory):
    return Medicine(name = name, inventory = inventory)

def create_default_medicine_unit(unit_id,med_id,unit_price):
    return MedicineUnit(
    unit_id=unit_id,
    medicine_id=med_id,
    unit_price=unit_price,
    is_default=True,
    )
def create_medicine_unit(unit_id,med_id,unit_price):
    return MedicineUnit(
    unit_id=unit_id,
    is_default=False,
    unit_price=unit_price,
    medicine_id=med_id,
    )
def create_unit_convert(med_id,default_unit_id,target_unit_id,convert_rate):
    return UnitConvert(
        med_id = med_id,
        default_unit_id = default_unit_id,
        target_unit_id = target_unit_id,
        convert_rate = convert_rate,
    )
def get_unit_convert_by_med_id_and_target_unit_id(med_id,target_unit_id):
    return UnitConvert.query.filter_by(med_id = med_id, target_unit_id = target_unit_id)

def get_medicine_units_by_med_id(med_id):
    return MedicineUnit.query.filter_by(medicine_id=med_id).all()


def updateunit_convert_rate(medicine,target_unit_id,convert_rate):
    unit_convert = get_unit_convert_by_med_id_and_target_unit_id(medicine.id,target_unit_id)
    unit_convert.convert_rate =convert_rate

    

def update_medicine_units(medicine,data):
    # Cập nhật các đơn vị khác
                # Lấy tất cả các đơn vị hiện tại của thuốc
                current_units = MedicineUnit.query.filter_by(medicine_id=medicine.id, is_default = False).all()

                # Tạo một tập hợp các unit_id có trong danh sách gửi từ giao diện
                incoming_unit_ids = None
                incoming_units = data.get('units', [])
                incoming_unit_ids = {int(unit['unit_id']) for unit in incoming_units} if incoming_units else set()

                default_unit_id = int(data.get('default_unit'))
                for unit in data.get('units', []):
                    unit_id = int(unit['unit_id'])
                    unit_price = float(unit['unit_price'])
                    unit_convert_rate = float(unit['convert_rate'])
                    existing_unit = get_medicice_unit_by_med_and_unit_id(medicine.id, unit_id)
                    if existing_unit:
                        existing_unit.unit_price = unit_price
                        updateunit_convert_rate(medicine,unit_id,unit_convert_rate)

                    else:
                        new_unit = create_medicine_unit(
                            unit_id,
                            medicine.id,
                            unit_price,
                        )
                        db.session.add(new_unit)
                        new_unit_convert = create_unit_convert(medicine.id,default_unit_id,unit_id,unit_convert_rate)
                        db.session.add(new_unit_convert)

                    # Lấy danh sách các quy đổi đơn vị hiện tại của thuốc
                existing_unit_converts = UnitConvert.query.filter_by(med_id=medicine.id).all()
                if not incoming_unit_ids: # nếu không có unit nào trên giao diện thì xóa hết unitconvert và
                    for unit_convert in existing_unit_converts:
                        db.session.delete(unit_convert)
                    for current_unit in current_units:
                        db.session.delete(current_unit)

                else:
                    for unit_convert in existing_unit_converts:
                        # Nếu đơn vị quy đổi không còn xuất hiện trong danh sách unit_ids từ giao diện, xóa nó
                        if unit_convert.target_unit_id not in incoming_unit_ids:
                            db.session.delete(unit_convert)

                    # Xóa các đơn vị đã không còn xuất hiện trong danh sách mới
                    for current_unit in current_units:
                        if current_unit.unit_id not in incoming_unit_ids:
                            db.session.delete(current_unit)

def get_bill_by_med_exam_id(med_exam_id):
    return Bill.query.filter_by(medical_exam_id=med_exam_id).first()

def convert_number_to_words(number):
    # Số int
    units = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    places = ["", "nghìn", "triệu", "tỷ"]

    def read_three_digits(n):
        if n == 0:
            return ""
        hundreds = n // 100
        tens_units = n % 100
        tens = tens_units // 10
        units_digit = tens_units % 10

        result = ""
        if hundreds > 0:
            result += units[hundreds] + " trăm "
        if tens > 1:
            result += units[tens] + " mươi "
            if units_digit == 1:
                result += "mốt"
            elif units_digit == 5:
                result += "lăm"
            elif units_digit != 0:
                result += units[units_digit]
        elif tens == 1:
            result += "mười "
            if units_digit == 5:
                result += "lăm"
            elif units_digit != 0:
                result += units[units_digit]
        else:
            if units_digit != 0:
                result += units[units_digit]
        return result.strip()

    if number == 0:
        return "không đồng"

    number_str = f"{number:,}".replace(",", "")
    groups = []
    while number > 0:
        groups.append(number % 1000)
        number //= 1000

    result = ""
    for i in range(len(groups)):
        if groups[i] != 0:
            result = read_three_digits(groups[i]) + " " + places[i] + " " + result
    result = result.strip() + " đồng"
    result = result[0].upper() + result[1:]  # Capitalize the first letter
    return result.strip()
#   số Float
#     def convert_number_to_words(number):
#     units = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
#     places = ["", "nghìn", "triệu", "tỷ"]

#     def read_three_digits(n):
#         if n == 0:
#             return ""
#         hundreds = n // 100
#         tens_units = n % 100
#         tens = tens_units // 10
#         units_digit = tens_units % 10

#         result = ""
#         if hundreds > 0:
#             result += units[hundreds] + " trăm "
#         if tens > 1:
#             result += units[tens] + " mươi "
#             if units_digit == 1:
#                 result += "mốt"
#             elif units_digit == 5:
#                 result += "lăm"
#             elif units_digit != 0:
#                 result += units[units_digit]
#         elif tens == 1:
#             result += "mười "
#             if units_digit == 5:
#                 result += "lăm"
#             elif units_digit != 0:
#                 result += units[units_digit]
#         else:
#             if units_digit != 0:
#                 result += "lẻ " + units[units_digit]
#         return result.strip()

#     def read_decimal(decimal_part):
#         result = ""
#         for digit in decimal_part:
#             result += units[int(digit)] + " "
#         return result.strip()

#     if number == 0:
#         return "không đồng"

#     integer_part = int(number)
#     decimal_part = str(round(number - integer_part, 2)).split(".")[1] if "." in str(number) else ""

#     # Xử lý phần nguyên
#     groups = []
#     while integer_part > 0:
#         groups.append(integer_part % 1000)
#         integer_part //= 1000

#     result = ""
#     for i in range(len(groups)):
#         if groups[i] != 0:
#             result = read_three_digits(groups[i]) + " " + places[i] + " " + result

#     result = result.strip() + " đồng"

#     # Xử lý phần thập phân
#     if decimal_part:
#         result += " và " + read_decimal(decimal_part) + " xu"

#     # Viết hoa chữ cái đầu tiên
#     result = result[0].upper() + result[1:]
#     return result.strip()

# # Nhập số tiền
# number = float(input("Nhập số tiền: "))
# print("Số tiền bằng chữ: " + convert_number_to_words(number))

