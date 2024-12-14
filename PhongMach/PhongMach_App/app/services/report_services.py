from sqlalchemy import func, distinct,case
from app.models import MedicalExam,Bill,Medicine,MedicineUnit,DetailExam,UnitConvert,Unit,Category
from config import Config
from app.extensions import db
from datetime import date

def count_patients_in_day(day, month,year):
    
    count = db.session.query(func.count(distinct(MedicalExam.patient_id)))\
        .filter(func.extract('year',MedicalExam.exam_day) == year)\
        .filter(func.extract('month',MedicalExam.exam_day) == month)\
        .filter(func.extract('day',MedicalExam.exam_day) == day).scalar()
    return count
def count_patients_in_month(year, month):
    """
    Đếm số lượng bệnh nhân duy nhất trong một tháng.
    :param year: Năm cần kiểm tra
    :param month: Tháng cần kiểm tra
    :return: Số lượng bệnh nhân
    """
    count = db.session.query(func.count(distinct(MedicalExam.patient_id)))\
        .filter(func.extract('year', MedicalExam.exam_day) == year)\
        .filter(func.extract('month', MedicalExam.exam_day) == month).scalar()
    return count

def get_total(medical_exam_info):
    total = 0
    for a in medical_exam_info['med_list']:
        total += float(a['price'])
    return total

def calculate_monthly_revenue(month, year):
    """
    Tính doanh thu của một tháng cụ thể trong năm.
    
    :param month: Tháng cần tính (1 - 12).
    :param year: Năm cần tính.
    :return: Tổng doanh thu của tháng.
    """
    revenue = 0
    revenue = db.session.query(func.sum(Bill.total))\
        .join(MedicalExam, Bill.medical_exam_id == MedicalExam.id)\
        .filter(func.extract('month', MedicalExam.exam_day) == month)\
        .filter(func.extract('year', MedicalExam.exam_day) == year)\
        .filter(Bill.is_pay == True)\
        .scalar()  # Lấy giá trị duy nhất
    
    return revenue
def get_daily_revenue(day, month, year):
    daily_revenue = db.session.query(func.sum(Bill.total))\
        .join(MedicalExam, Bill.medical_exam_id == MedicalExam.id)\
        .filter(func.extract('year', MedicalExam.exam_day) == year)\
        .filter(func.extract('month', MedicalExam.exam_day) == month)\
        .filter(func.extract('day', MedicalExam.exam_day) == day)\
        .filter(Bill.is_pay == True)\
        .scalar()
    
    return daily_revenue or 0

def get_monthly_revenue( month, year):
    monthly_revenue = db.session.query(func.sum(Bill.total))\
        .join(MedicalExam, Bill.medical_exam_id == MedicalExam.id)\
        .filter(func.extract('year', MedicalExam.exam_day) == year)\
        .filter(func.extract('month', MedicalExam.exam_day) == month)\
        .filter(Bill.is_pay == True)\
        .scalar()
    
    return monthly_revenue or 0

def count_medicine_by_category(month, year, category_id):
   
    result = db.session.query(
        Medicine.name.label("medicine_name"),
        func.sum(
            case(
                (UnitConvert.default_unit_id != Unit.id,DetailExam.quantity * UnitConvert.convert_rate),
                else_=DetailExam.quantity  # Nếu không có quy đổi, giữ nguyên số lượng
            )
        ).label("total_quantity")
    ).join(MedicineUnit, DetailExam.medicine_id == MedicineUnit.medicine_id) \
     .join(UnitConvert, DetailExam.unit_id == UnitConvert.target_unit_id) \
     .join(Unit, MedicineUnit.unit_id == Unit.id) \
     .join(Medicine, DetailExam.medicine_id == Medicine.id) \
     .join(Category, Medicine.categories) \
     .join(MedicalExam, DetailExam.medical_exam_id == MedicalExam.id) \
     .join(Bill, MedicalExam.id == Bill.medical_exam_id) \
     .filter(
         func.extract("month", MedicalExam.exam_day) == month,
         func.extract("year", MedicalExam.exam_day) == year,
         Category.id == category_id,
         Bill.is_pay == True
     ).group_by(Medicine.id).all()
    
    return result