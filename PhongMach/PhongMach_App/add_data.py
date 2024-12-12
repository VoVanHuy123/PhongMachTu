from datetime import date, time
from app import create_app, db  # Thay "PhongMach_App" bằng tên module ứng dụng của bạn
from app.models import * # Thay đổi đường dẫn nếu cần
from datetime import time, timedelta

# Khởi tạo ứng dụng
app = create_app()  # Đảm bảo hàm `create_app()` của bạn được định nghĩa để trả về một ứng dụng Flask

# Mở ngữ cảnh ứng dụng
if __name__ == "__main__":
    with app.app_context():

        
    #     doctor_account = Account(
    #         user_name="bacsi123",
    #         password="c4ca4238a0b923820dcc509a6f75849b"
    #     )

    # # Tạo bác sĩ
    #     doctor = Doctor(
    #         last_name="Nguyễn",
    #         first_name="Văn A",
    #         gender="Nam",
    #         birth_day=date(1985, 7, 15),
    #         email="bacsi123@example.com",
    #         image="hinh_anh.jpg",
    #         account=doctor_account,  # Liên kết với tài khoản
    #         specialty="Tim mạch",  # Chuyên khoa
    #         degree="Tiến sĩ Y học",  # Học vị
    #         experience="10 năm tại Bệnh viện Trung ương",  # Kinh nghiệm
    #         current_workplace="Bệnh viện Trung ương"  # Nơi làm việc hiện tại
    #     )
    



# Hàm tạo ExamTime từ 8h đến 16h với thời gian mỗi kỳ thi là 30 phút
        # def create_exam_times():
        #     # Khởi tạo thời gian bắt đầu và kết thúc
        #     start_time = time(8, 0)  # Bắt đầu từ 8:00 AM
        #     end_time = time(16, 0)  # Kết thúc lúc 16:00 PM
        #     current_time = start_time
            
        #     # Lặp qua các khoảng thời gian từ 8h đến 16h với mỗi kỳ thi kéo dài 30 phút
        #     while current_time < end_time:
        #         next_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()
                
        #         # Tạo đối tượng ExamTime cho mỗi khoảng thời gian
        #         exam_time = ExamTime(
        #             start_time=current_time,
        #             end_time=next_time
        #         )
                
        #         # Thêm vào cơ sở dữ liệu
        #         db.session.add(exam_time)
                
        #         # Cập nhật current_time cho kỳ thi tiếp theo
        #         current_time = next_time
            
        #     # Commit vào cơ sở dữ liệu
        #         db.session.commit()

        #         print("Các thời gian thi đã được tạo thành công!")

# # Gọi hàm để tạo dữ liệu
        # create_exam_times()

        
        # units = [
        #     Unit(id=1, name="Viên"),
        #     Unit(id=2, name="Ống"),
        #     Unit(id=3, name="Hộp"),
        #     Unit(id=4, name="Chai"),
        #     Unit(id=5, name="Gói"),
        #     Unit(id=6, name="Lọ"),
        #     Unit(id=7, name="Gram"),
        #     Unit(id=8, name="Mililit"),
        #     Unit(id=9, name="Vỉ"),
        #     Unit(id=10, name="Kg"),
        # ]

        # medicines = [
        #     Medicine(id=1, name="Paracetamol", inventory=100),
        #     Medicine(id=2, name="Amoxicillin", inventory=200),
        #     Medicine(id=3, name="Vitamin C", inventory=150),
        #     Medicine(id=4, name="Erythromycin", inventory=50),
        #     Medicine(id=5, name="Ibuprofen", inventory=120),
        #     Medicine(id=6, name="Ceftriaxone", inventory=30),
        #     Medicine(id=7, name="Ciprofloxacin", inventory=70),
        #     Medicine(id=8, name="Metronidazole", inventory=90),
        #     Medicine(id=9, name="Salbutamol", inventory=110),
        #     Medicine(id=10, name="Loperamide", inventory=140),
        # ]

        # medicine_units = [
        #     MedicineUnit(medicine_id=1, unit_id=1, is_default=True, unit_price=5000),
        #     MedicineUnit(medicine_id=2, unit_id=9, is_default=True, unit_price=10000),
        #     MedicineUnit(medicine_id=3, unit_id=1, is_default=True, unit_price=7000),
        #     MedicineUnit(medicine_id=4, unit_id=2, is_default=True, unit_price=20000),
        #     MedicineUnit(medicine_id=5, unit_id=1, is_default=True, unit_price=15000),
        #     MedicineUnit(medicine_id=6, unit_id=2, is_default=True, unit_price=30000),
        #     MedicineUnit(medicine_id=7, unit_id=3, is_default=True, unit_price=25000),
        #     MedicineUnit(medicine_id=8, unit_id=4, is_default=True, unit_price=10000),
        #     MedicineUnit(medicine_id=9, unit_id=2, is_default=True, unit_price=8000),
        #     MedicineUnit(medicine_id=10, unit_id=5, is_default=True, unit_price=6000),
        # ]

        # categories = [
        #     Category(id=1, name="Thuốc giảm đau"),
        #     Category(id=2, name="Thuốc kháng sinh"),
        #     Category(id=3, name="Vitamin và khoáng chất"),
        #     Category(id=4, name="Thuốc chống viêm"),
        #     Category(id=5, name="Thuốc hạ sốt"),
        #     Category(id=6, name="Thuốc điều trị đường hô hấp"),
        #     Category(id=7, name="Thuốc tiêu hóa"),
        #     Category(id=8, name="Thuốc dị ứng"),
        #     Category(id=9, name="Thuốc tim mạch"),
        #     Category(id=10, name="Thuốc bổ sung dinh dưỡng"),
        # ]

        # medicine_categories = [
        #     {"medicine_id": 1, "category_id": 1},  # Paracetamol - Thuốc giảm đau
        #     {"medicine_id": 1, "category_id": 5},  # Paracetamol - Thuốc hạ sốt
        #     {"medicine_id": 2, "category_id": 2},  # Amoxicillin - Thuốc kháng sinh
        #     {"medicine_id": 3, "category_id": 3},  # Vitamin C - Vitamin và khoáng chất
        #     {"medicine_id": 4, "category_id": 2},  # Erythromycin - Thuốc kháng sinh
        #     {"medicine_id": 4, "category_id": 4},  # Erythromycin - Thuốc chống viêm
        #     {"medicine_id": 5, "category_id": 4},  # Ibuprofen - Thuốc chống viêm
        #     {"medicine_id": 6, "category_id": 2},  # Ceftriaxone - Thuốc kháng sinh
        #     {"medicine_id": 6, "category_id": 6},  # Ceftriaxone - Thuốc điều trị đường hô hấp
        #     {"medicine_id": 7, "category_id": 2},  # Ciprofloxacin - Thuốc kháng sinh
        #     {"medicine_id": 8, "category_id": 7},  # Metronidazole - Thuốc tiêu hóa
        #     {"medicine_id": 9, "category_id": 6},  # Salbutamol - Thuốc điều trị đường hô hấp
        #     {"medicine_id": 10, "category_id": 7}, # Loperamide - Thuốc tiêu hóa
        #     {"medicine_id": 10, "category_id": 8}, # Loperamide - Thuốc dị ứng
        # ]

        # unit_convert = UnitConvert(
        #     med_id=1,  # ID của thuốc
        #     default_unit_id=1,  # ID của đơn vị 'Viên'
        #     target_unit_id=8,  # ID của đơn vị 'Mililit'
        #     convert_rate=10  # Tỷ lệ chuyển đổi
        # )

        # # Thêm dữ liệu vào database
        # try:
        #     # Thêm đơn vị đo lường
        #     db.session.add_all(units)
        #     # Thêm danh mục thuốc
        #     db.session.add_all(categories)
        #     # Thêm thuốc
        #     db.session.add_all(medicines)
        #     db.session.commit()  # Lưu dữ liệu bảng chính trước

        #     # Thêm liên kết thuốc và loại thuốc
        #     for mc in medicine_categories:
        #         db.session.execute(med_category.insert().values(medicine_id=mc["medicine_id"], category_id=mc["category_id"]))
            
        #     # Thêm các đơn vị thuốc
        #     db.session.add_all(medicine_units)

        #     # Thêm dữ liệu chuyển đổi đơn vị
        #     db.session.add(unit_convert)

        #     # Lưu tất cả thay đổi
        #     db.session.commit()
        #     print("Thêm dữ liệu thành công!")
        # except Exception as e:
        #     db.session.rollback()
        #     print(f"Lỗi khi thêm dữ liệu: {e}")

        unit = MedicineUnit(medicine_id=1, unit_id=8, is_default=False, unit_price=20000)
        db.session.add(unit)
        db.session.commit()

            