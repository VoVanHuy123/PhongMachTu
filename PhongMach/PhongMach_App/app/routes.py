from flask import Blueprint, render_template
from .services.user_services import get_doctors


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# @main.route('/appointment')
# def appointment():
#     doctors = get_doctors()
#     return render_template('appointment/appointment.html', doctors=doctors)