from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from app.forms.admin import ScheduleForm
from app.models.schedule import Schedule
from app.models.group import Group
from app import db
from functools import wraps

teacher_bp = Blueprint('teacher', __name__)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@teacher_bp.route('/teacher/schedule', methods=['GET'])
@login_required
@role_required('teacher')
def teacher_schedule():
    schedules = Schedule.query.join(Group).filter(Group.teacher_id == current_user.id).all()
    return render_template('teacher_schedule.html', schedules=schedules)

@teacher_bp.route('/teacher/schedule', methods=['POST'])
@login_required
@role_required('teacher')
def teacher_add_schedule():
    form = ScheduleForm(teacher_id=current_user.id)
    if form.validate_on_submit():
        new_schedule = Schedule(
            subject=form.subject.data,
            time=form.time.data,
            group_id=form.group_id.data
        )
        db.session.add(new_schedule)
        db.session.commit()
        flash('Занятие добавлено!', 'success')
        return redirect(url_for('teacher.teacher_schedule'))
    return render_template('add_schedule.html', form=form)

@teacher_bp.route('/teacher/schedule/<int:schedule_id>', methods=['DELETE'])
@login_required
@role_required('teacher')
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.group.teacher_id != current_user.id:
        abort(403)
    db.session.delete(schedule)
    db.session.commit()
    flash('Занятие удалено', 'success')
    return '', 204

@teacher_bp.route('/teacher/schedule/<int:schedule_id>', methods=['PATCH'])
@login_required
@role_required('teacher')
def edit_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.group.teacher_id != current_user.id:
        abort(403)
    form = ScheduleForm(teacher_id=current_user.id, obj=schedule)
    if form.validate_on_submit():
        schedule.subject = form.subject.data
        schedule.time = form.time.data
        schedule.group_id = form.group_id.data
        db.session.commit()
        flash('Занятие обновлено!', 'success')
        return redirect(url_for('teacher.teacher_schedule'))
    return render_template('edit_schedule.html', form=form, schedule=schedule)