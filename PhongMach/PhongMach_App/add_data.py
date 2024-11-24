from datetime import date, time
from app import create_app, db  # Thay "PhongMach_App" bằng tên module ứng dụng của bạn
from app.models import Doctor,User,PhoneNumber, ExamTime , Account # Thay đổi đường dẫn nếu cần

# Khởi tạo ứng dụng
app = create_app()  # Đảm bảo hàm `create_app()` của bạn được định nghĩa để trả về một ứng dụng Flask

# Mở ngữ cảnh ứng dụng
if __name__ == "__main__":
    with app.app_context():

        account = Account.query.first()

    # Tạo người dùng (User) cho bác sĩ
        # doctor = Doctor(
        #     last_name="Hà",
        #     first_name="Thị E",
        #     gender="Female",
        #     birth_day=date(1987, 3, 18),
        #     email="HaThiE@gmail.com",
        #     image="doctor4.jpg",
        #     account_id=account.id,  # Liên kết User với Account
        #     specialty="Thần Kinh",
        #     experience="Hơn 12 năm kinh nghiệm làm bác sĩ",
        #     current_workplace="Bệnh viện Chợ Rẫy",
        # )
        

        

        # db.session.add(doctor)  # Thêm Doctor vào cơ sở dữ liệu
        # db.session.commit()  # Commit để lưu Doctor vào cơ sở dữ liệu

        # print("Bác sĩ đã được thêm thành công!")


        # Lấy tài khoản đã được tạo
        

        # Tạo người dùng (User) cho bác sĩ
       

         # Commit để lưu tài khoản vào cơ sở dữ liệu
        # Tạo bác sĩ (Doctor) với thông tin chuyên môn
        doctor = Doctor(
            last_name="Hà",
            first_name="Thị E",
            gender="Female",
            birth_day=date(1987, 3, 18),
            email="HaThiE@gmail.com",
            image="doctor4.jpg",
            specialty="Thần Kinh",
            experience="Hơn 12 năm kinh nghiệm làm bác sĩ",
            current_workplace="Bệnh viện Chợ Rẫy",
            role = "doctor",
            
        )
        account = Account(
            user_name="bacsib",
            password="12345",
            active=True,
            )
        

        # Lưu Account vào cơ sở dữ liệu
        db.session.add(account)
        db.session.commit()  # Commit để lưu Account

        # Gán account cho doctor
        doctor.account_id = account.id  # Liên kết Doctor với Account

        # Thêm Doctor vào cơ sở dữ liệu
        db.session.add(doctor)
        db.session.commit()  # Commit để lưu Doctor vào cơ sở dữ liệu

        print("Bác sĩ đã được thêm thành công!")
        