from flask import Blueprint, render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from app.forms.admin import UserForm, GroupForm, StudentForm, ScheduleForm
from app.models.account import Account
from app.models.group import Group
from app.models.schedule import Schedule
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@admin_bp.route('/admin', methods=['GET'])
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin/admin.html')

@admin_bp.route('/users', methods=['GET'])
@login_required
@role_required('admin')
def get_users():
    users = Account.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users', methods=['POST'])
@login_required
@role_required('admin')
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Account(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            group_id=form.group_id.data if form.role.data == 'student' else None
        )
        user.set_password(form.password.data)  # Устанавливаем пароль через метод
        db.session.add(user)
        db.session.commit()
        flash('Пользователь создан.', 'success')
        return redirect(url_for('admin.get_users'))
    return render_template('admin/create_user.html', form=form)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])  # Изменён путь
@login_required
@role_required('admin')
def update_user(user_id):
    user = Account.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data or user.username
        user.email = form.email.data or user.email
        user.role = form.role.data or user.role
        user.group_id = form.group_id.data if form.role.data == 'student' else None
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Данные пользователя обновлены!', 'success')
        return redirect(url_for('admin.get_users'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])  # Изменён путь
@login_required
@role_required('admin')
def delete_user(user_id):
    user = Account.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь удалён!', 'success')
    return redirect(url_for('admin.get_users'))

@admin_bp.route('/groups', methods=['GET'])
@login_required
@role_required('admin')
def get_groups():
    groups = Group.query.all()
    form = GroupForm()
    return render_template('admin/groups.html', groups=groups, form=form)

@admin_bp.route('/groups', methods=['POST'])
@login_required
@role_required('admin')
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(group)
        db.session.commit()
        flash('Группа создана.', 'success')
        return redirect(url_for('admin.get_groups'))
    return render_template('admin/groups.html', groups=Group.query.all(), form=form)

@admin_bp.route('/groups/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def update_group(group_id):
    group = Group.query.get_or_404(group_id)
    form = GroupForm(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('Группа обновлена.', 'success')
        return redirect(url_for('admin.get_groups'))
    return render_template('admin/edit_group.html', form=form, group=group)

@admin_bp.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    Account.query.filter_by(group_id=group_id).update({'group_id': None})
    db.session.delete(group)
    db.session.commit()
    flash('Группа удалена.', 'success')
    return redirect(url_for('admin.get_groups'))

@admin_bp.route('/groups/<int:group_id>/students', methods=['GET'])
@login_required
@role_required('admin')
def group_students(group_id):
    group = Group.query.get_or_404(group_id)
    students = Account.query.filter_by(group_id=group_id, role='student').all()
    return render_template('group_students.html', group=group, students=students)

@admin_bp.route('/students/<int:student_id>', methods=['PATCH'])
@login_required
@role_required('admin')
def update_student(student_id):
    student = Account.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.username = form.username.data
        student.email = form.email.data
        student.group_id = form.group_id.data
        db.session.commit()
        flash('Данные студента обновлены.', 'success')
        return redirect(url_for('admin.group_students', group_id=student.group_id))
    return render_template('admin/edit_student.html', form=form, student=student)

@admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_student(student_id):
    student = Account.query.get_or_404(student_id)
    group_id = student.group_id
    db.session.delete(student)
    db.session.commit()
    flash('Студент удалён.', 'success')
    return redirect(url_for('admin.group_students', group_id=group_id))

@admin_bp.route('/schedule', methods=['GET'])
@login_required
@role_required('admin')
def view_schedule():
    schedules = Schedule.query.all()
    return render_template('view_schedule.html', schedules=schedules)

