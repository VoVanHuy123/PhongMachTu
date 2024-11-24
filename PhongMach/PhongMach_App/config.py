import os
import secrets
import cloudinary
SECRET_KEY = secrets.token_hex(32)  # Chuỗi ngẫu nhiên dài 32 byte



class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' lưu trong .venv
    SECRET_KEY = secrets.token_hex(32)  # Chuỗi ngẫu nhiên dài 32 byte
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'  
    #                          đổi  ten-admin-Mysql:mật-khẩu              tên database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:442161@localhost:3306/phongmach?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PAGE_SIZE = 2

    def init_cloudinary():
        cloudinary.config(
            cloud_name="dnzjjdg0v",
            api_key="123958894742992",
            api_secret="kQugdU7BMnVH5E4OYtFLvGKrHfk",
        )