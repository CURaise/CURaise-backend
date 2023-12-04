import os

from flask import Flask

from config import Config
from src.extensions import db
from src.extensions import login_manager
from src.extensions import firebase_admin, auth

from dotenv import load_dotenv

# Imports for creating the tables. DO NOT remove them for import optimization...
from src.models.admin import Admin
from src.models.club import Club
from src.models.fundraiser import Fundraiser
from src.models.fundraiser_item import FundraiserItem
from src.models.student import Student
from src.models.transaction import Transaction


def create_app(config=Config()):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = os.environ['FLASK_SECUREKEY']

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user):
        user_info = str(user).split('_')
        user_type, user_id = user_info[0], user_info[1]
        if user_type == 'club':
            return Club.query.get({'id': user_id})
        elif user_type == 'admin':
            return Admin.query.get({'id': user_id})
        elif user_type == 'student':
            return Student.query.get({'id': user_id})
        else:
            return None

    from src.clubs import bp as clubs_bp
    app.register_blueprint(blueprint=clubs_bp, url_prefix='/api/clubs')

    from src.fundraisers import bp as fundraisers_bp
    app.register_blueprint(blueprint=fundraisers_bp, url_prefix='/api/fundraisers')

    from src.students import bp as students_bp
    app.register_blueprint(blueprint=students_bp, url_prefix='/api/students')

    from src.transactions import bp as transactions_bp
    app.register_blueprint(blueprint=transactions_bp, url_prefix='/api/transactions')

    from src.admin import bp as admin_bp
    app.register_blueprint(blueprint=admin_bp, url_prefix='/api/admin')

    from src.main import bp as main_bp
    app.register_blueprint(blueprint=main_bp, url_prefix='/api')

    return app
