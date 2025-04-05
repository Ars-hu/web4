from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from app.models.group import Group

class UserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Роль', choices=[('admin', 'Администратор'), ('student', 'Студент'), ('teacher', 'Преподаватель')], validators=[DataRequired()])
    group_id = SelectField('Группа', coerce=int, validators=[Optional()])
    password = PasswordField('Новый пароль', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Подтверждение нового пароля', validators=[Optional(), EqualTo('password')])
    submit = SubmitField('Сохранить изменения')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.group_id.choices = [(g.id, g.name) for g in Group.query.all()]

class GroupForm(FlaskForm):
    name = StringField('Название группы', validators=[DataRequired()])
    description = StringField('Описание группы', validators=[DataRequired()])
    submit = SubmitField('Создать группу')

class StudentForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.group_id.choices = [(g.id, g.name) for g in Group.query.all()]

class ScheduleForm(FlaskForm):
    subject = StringField('Предмет', validators=[DataRequired()])
    time = DateTimeField('Дата и время', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Создать')

    def __init__(self, teacher_id=None, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        if teacher_id:
            self.group_id.choices = [(g.id, g.name) for g in Group.query.filter_by(teacher_id=teacher_id).all()]
        else:
            self.group_id.choices = [(g.id, g.name) for g in Group.query.all()]