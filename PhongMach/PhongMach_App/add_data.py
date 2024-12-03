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
    



# # Hàm tạo ExamTime từ 8h đến 16h với thời gian mỗi kỳ thi là 30 phút
#         def create_exam_times():
#             # Khởi tạo thời gian bắt đầu và kết thúc
#             start_time = time(8, 0)  # Bắt đầu từ 8:00 AM
#             end_time = time(16, 0)  # Kết thúc lúc 16:00 PM
#             current_time = start_time
            
#             # Lặp qua các khoảng thời gian từ 8h đến 16h với mỗi kỳ thi kéo dài 30 phút
#             while current_time < end_time:
#                 next_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()
                
#                 # Tạo đối tượng ExamTime cho mỗi khoảng thời gian
#                 exam_time = ExamTime(
#                     start_time=current_time,
#                     end_time=next_time
#                 )
                
#                 # Thêm vào cơ sở dữ liệu
#                 db.session.add(exam_time)
                
#                 # Cập nhật current_time cho kỳ thi tiếp theo
#                 current_time = next_time
            
#             # Commit vào cơ sở dữ liệu
#                 db.session.commit()

#                 print("Các thời gian thi đã được tạo thành công!")

# # Gọi hàm để tạo dữ liệu
#         create_exam_times()


        units = [
            Unit(id=1, unit="Viên"),
            Unit(id=2, unit="Ống"),
            Unit(id=3, unit="Hộp"),
            Unit(id=4, unit="Chai"),
            Unit(id=5, unit="Gói"),
            Unit(id=6, unit="Lọ"),
            Unit(id=7, unit="Gram"),
            Unit(id=8, unit="Mililit"),
            Unit(id=9, unit="Vỉ"),
            Unit(id=10, unit="Kg"),
        ]
        medicines = [
            Medicine(id=1, name="Paracetamol", inventory=100, unit_price=5000),
            Medicine(id=2, name="Amoxicillin", inventory=200, unit_price=7000),
            Medicine(id=3, name="Vitamin C", inventory=150, unit_price=6000),
            Medicine(id=4, name="Erythromycin", inventory=50, unit_price=10000),
            Medicine(id=5, name="Ibuprofen", inventory=120, unit_price=8000),
            Medicine(id=6, name="Ceftriaxone", inventory=30, unit_price=20000),
            Medicine(id=7, name="Ciprofloxacin", inventory=70, unit_price=15000),
            Medicine(id=8, name="Metronidazole", inventory=90, unit_price=9000),
            Medicine(id=9, name="Salbutamol", inventory=110, unit_price=5000),
            Medicine(id=10, name="Loperamide", inventory=140, unit_price=4000),
        ]
        medicine_units = [
            MedicineUnit(medicine_id=1, unit_id=1, is_default = True),
            MedicineUnit(medicine_id=2, unit_id=9, is_default = True),
            MedicineUnit(medicine_id=3, unit_id=1, is_default = True),
            MedicineUnit(medicine_id=4, unit_id=2, is_default = True),
            MedicineUnit(medicine_id=5, unit_id=1, is_default = True),
            MedicineUnit(medicine_id=6, unit_id=2, is_default = True),
            MedicineUnit(medicine_id=7, unit_id=3, is_default = True),
            MedicineUnit(medicine_id=8, unit_id=4, is_default = True),
            MedicineUnit(medicine_id=9, unit_id=2, is_default = True),
            MedicineUnit(medicine_id=10, unit_id=5, is_default = True), 
        ]


        
        # Lưu vào cơ sở dữ liệu
        db.session.commit()


            