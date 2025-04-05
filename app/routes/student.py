from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.schedule import Schedule
from functools import wraps

student_bp = Blueprint('student', __name__)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@student_bp.route('/student/schedule', methods=['GET'])
@login_required
@role_required('student')
def student_schedule():
    if not current_user.group:
        flash('Вы не состоите в группе', 'error')
        return redirect(url_for('student.index'))
    schedules = Schedule.query.filter_by(group_id=current_user.group_id).all()
    return render_template('schedule.html', schedules=schedules)

@student_bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')