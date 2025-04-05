from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Регистрация blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.teacher import teacher_bp
    from app.routes.student import student_bp

    app.register_blueprint(auth_bp, url_prefix='/app/v1')
    app.register_blueprint(admin_bp, url_prefix='/app/v1')
    app.register_blueprint(teacher_bp, url_prefix='/app/v1')
    app.register_blueprint(student_bp, url_prefix='/app/v1')

    # Глобальный маршрут для корневого пути
    @app.route('/', methods=['GET'])
    def root():
        return render_template('index.html')  # Или перенаправление, например, return redirect('/app/v1/')

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.account import Account
        return Account.query.get(int(user_id))

    with app.app_context():
        db.create_all()  # Временно, позже использовать миграции

    return app