import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres:+-++@localhost:5432/postgres'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False