import sys
from app import Config  # Import Config từ app (nơi chứa config.py)
# from app.extensions import twilio_client
from twilio.base.exceptions import TwilioRestException

from config import Config

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