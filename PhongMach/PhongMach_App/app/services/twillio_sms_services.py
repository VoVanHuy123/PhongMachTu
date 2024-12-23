import sys
from app import Config  # Import Config từ app (nơi chứa config.py)
# from app.extensions import twilio_client
from twilio.base.exceptions import TwilioRestException
from flask_mail import Message
from ..extensions import mail
from threading import Thread
from config import Config

from app import create_app
# app = create_app()


def send_sms( message):
    pass
    # try:
    #     message = twilio_client.messages.create(
    #         body=message,
    #         from_=Config.TWILIO_PHONE_NUMBER,
    #         to='+84862982784'
    #     )
    #     return f"Message sent successfully with SID: {message.sid}"  # Trả về SID nếu gửi thành công
    # except TwilioRestException as e:
    #     # Lỗi từ Twilio (ví dụ: số không hợp lệ)
    #     return f"Failed to send SMS. Twilio Error: {e.msg} (Status Code: {e.status})"
    # except Exception as e:
    #     # Lỗi chung
    #     return f"Failed to send SMS. Error: {str(e)}"

# @celery.task
# def send_email(subject, recipients, body, html=None):
#     """Gửi email bất đồng bộ bằng Celery."""
#     try:
#         msg = Message(subject=subject, recipients=recipients, body=body, html=html)
#         mail.send(msg)
#         print(f"Email sent to {recipients}")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

def send_email_async(app, subject, recipients, body,html=None):
    with app.app_context():
        try:
            msg = Message(subject=subject, recipients=recipients, body=body, html=html)
            mail.send(msg)
            print(f"Email sent to {recipients}")
        except Exception as e:
            print(f"Failed to send email: {e}")

def send_email_in_thread(app, subject, recipients, message):
    thread = Thread(target=send_email_async, args=(app, subject, recipients, message))
    thread.start()