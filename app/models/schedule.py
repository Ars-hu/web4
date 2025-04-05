from app import db

class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)