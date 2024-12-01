from datetime import date, time
from app import create_app, db  # Thay "PhongMach_App" bằng tên module ứng dụng của bạn
from app.models import * # Thay đổi đường dẫn nếu cần

# Khởi tạo ứng dụng
app = create_app()  # Đảm bảo hàm `create_app()` của bạn được định nghĩa để trả về một ứng dụng Flask

# Mở ngữ cảnh ứng dụng
if __name__ == "__main__":
    with app.app_context():

        

   
        # doctor = Doctor(
        #     last_name="Hà",
        #     first_name="Thị E",
        #     gender="Female",
        #     birth_day=date(1987, 3, 18),
        #     email="HaThiE@gmail.com",
        #     image="doctor4.jpg",
        #     specialty="Thần Kinh",
        #     experience="Hơn 12 năm kinh nghiệm làm bác sĩ",
        #     current_workplace="Bệnh viện Chợ Rẫy",
        #     role = "doctor",
            
        # )
        # account = Account(
        #     user_name="bacsib",
        #     password="12345",
        #     active=True,
        #     )
        
        med = Medicine.query.get(5)

        
        unit = MedicineUnit.query.get(1)

        med.units.append(unit)
        db.session.commit()

        print("Bác sĩ đã được thêm thành công!")
        