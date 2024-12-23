from sqlalchemy import func, distinct,case
# from sqlalchemy.sql.expression  import coalesce
from app.models import MedicalExam,Bill,Medicine,MedicineUnit,DetailExam,UnitConvert,Unit,Category,med_category
from config import Config
from app.extensions import db
from datetime import date,datetime

def count_patients_in_day(day, month,year):
    
    count = db.session.query(func.count(distinct(MedicalExam.patient_id)))\
        .filter(func.extract('year',MedicalExam.exam_day) == year)\
        .filter(func.extract('month',MedicalExam.exam_day) == month)\
        .filter(func.extract('day',MedicalExam.exam_day) == day).scalar(    )
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
        .filter(func.extract('year', Bill.created_date) == year)\
        .filter(func.extract('month', Bill.created_date) == month)\
        .filter(func.extract('day', Bill.created_date) == day)\
        .filter(Bill.is_pay == True)\
        .scalar()
    
    return daily_revenue or 0

def get_monthly_revenue( month, year=datetime.today().year):
    monthly_revenue = db.session.query(func.sum(Bill.total))\
        .filter(func.extract('year', Bill.created_date) == year)\
        .filter(func.extract('month', Bill.created_date) == month)\
        .filter(Bill.is_pay == True)\
        .scalar()
    
    return monthly_revenue or 0

#quarter/month
def get_revenue(time,year = datetime.today().year):
    # Truy vấn doanh thu cho 12 tháng trong năm
    total_revenue = db.session.query(
        func.extract(time, Bill.created_date).label(time),
        func.sum(Bill.total).label('revenue')
    )\
    .filter(func.extract('year', Bill.created_date) == year)\
    .filter(Bill.is_pay == True )\
    .group_by(func.extract(time, Bill.created_date))\
    .order_by(func.extract(time, Bill.created_date))\
    .all()
    return total_revenue


def get_medicine_sold_report(month, year, category_id):
    
    result = (
    db.session.query(
        Medicine.name.label("medicine_name"),
        func.sum(
            case(
                
                    (
                        UnitConvert.default_unit_id != Unit.id,
                        DetailExam.quantity * UnitConvert.convert_rate,
                    ),
                else_=DetailExam.quantity,
            )
            
        ).label("total_quantity"),
    )
    .outerjoin(DetailExam, DetailExam.medicine_id == Medicine.id)
    .join(Unit, DetailExam.unit_id == Unit.id)
    .outerjoin(
        UnitConvert,
        (DetailExam.medicine_id == UnitConvert.med_id) &
        (DetailExam.unit_id == UnitConvert.target_unit_id),
    )
    .join(MedicalExam, DetailExam.medical_exam_id == MedicalExam.id)
    .join(Bill, MedicalExam.id == Bill.medical_exam_id)
    .join(Category, Medicine.categories)
    .filter(
        func.extract("month", MedicalExam.exam_day) == month,
        func.extract("year", MedicalExam.exam_day) == year,
        Category.id == category_id,
        (Bill.is_pay == True) | (Bill.is_pay.is_(None)),
    )
    .group_by(Medicine.id).all()
    )
    
    return result

# lấy số lượng thuốc mội loại thuốc
def get_medicine_of_category():
    
    results = db.session.query(
        Category.name,
        func.count(Medicine.id)
    ).outerjoin(Medicine.categories).group_by(Category.name).all()
    return results

#lấy số lượng của từng thuốc của 1 loại thuốc
def get_num_med_of_category(cate_id):
    medicines = (
        db.session.query(
            Medicine.id, 
            Medicine.name,
            Unit.name,
            func.sum(Medicine.inventory).label("total_inventory")
        )
        .join(Category.medicines)\
        .join(MedicineUnit, Medicine.id == MedicineUnit.medicine_id)
        .join(Unit, Unit.id == MedicineUnit.unit_id)
        .filter(Category.id == cate_id,
                MedicineUnit.is_default == True
                )
        .group_by(Medicine.id,Unit.name)
        .all()
    )
    return medicines
# def get_num_med_of_category(cate_id):
#     medicines = (
#         db.session.query(
#             Medicine.id, 
#             Medicine.name,
#             func.sum(Medicine.inventory).label("total_inventory")
#         )
#         .join(Category.medicines)
#         .filter(Category.id == cate_id,
#                 )
#         .group_by(Medicine.id)
#         .all()
#     )
#     return medicines