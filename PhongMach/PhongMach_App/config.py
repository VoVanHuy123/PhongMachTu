import os
import secrets
import cloudinary
from flask_mail import Mail, Message
from dotenv import load_dotenv
from celery import Celery
load_dotenv() 



class Config:
    SECRET_KEY = secrets.token_hex(32)  # Chuỗi ngẫu nhiên dài 32 byte
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:442161@localhost:3306/phongmach?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PAGE_SIZE = 2

 
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS= True
    MAIL_USERNAME= 'hieu96537@gmail.com'
    MAIL_PASSWORD= 'rowzloajbqkimrpi'#rowz loaj bqki mrpi
    MAIL_DEFAULT_SENDER= 'hieu96537@gmail.com'
    # CELERY_BROKER_URL= 'redis://localhost:6379/0'#redis://localhost:6379/0'  # Redis làm broker
    # CELERY_RESULT_BACKEND=None # 'redis://localhost:6379/0'

    def init_cloudinary():
        cloudinary.config(
            cloud_name="dnzjjdg0v",
            api_key="123958894742992",
            api_secret="kQugdU7BMnVH5E4OYtFLvGKrHfk",
        )
   