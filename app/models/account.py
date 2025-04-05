from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Account(UserMixin, db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='student')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)

    group = db.relationship('Group', foreign_keys=[group_id], backref='students')
    taught_groups = db.relationship('Group', foreign_keys='Group.teacher_id', backref='teacher')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)