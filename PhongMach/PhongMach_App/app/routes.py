from flask import Blueprint, render_template,jsonify
from .services.user_services import get_doctors
from .services.medical_services import *


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# @main.route('/appointment')
# def appointment():
#     doctors = get_doctors()
#     return render_template('appointment/appointment.html', doctors=doctors)

@main.route('/api/units', methods=['GET'])
def get_units_api():
    units = get_units()
    return jsonify([{'id': unit.id, 'name': unit.name} for unit in units])