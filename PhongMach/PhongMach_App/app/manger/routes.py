from flask import Blueprint, render_template

manager = Blueprint('manager', __name__, url_prefix='/manager')

@manager.route('/')
def manager_run():
    return render_template('manger.html')
