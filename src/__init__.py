from flask import Flask

from config import Config
from src.extensions import db

from dotenv import load_dotenv

# Imports for creating the tables. DO NOT remove them for import optimization...
from src.models.club import Club
from src.models.fundraiser import Fundraiser
from src.models.fundraiser_item import FundraiserItem
from src.models.student import Student
from src.models.transaction import Transaction


def create_app(config=Config()):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from src.clubs import bp as clubs_bp
    app.register_blueprint(blueprint=clubs_bp, url_prefix='/clubs')

    from src.fundraisers import bp as fundraisers_bp
    app.register_blueprint(blueprint=fundraisers_bp, url_prefix='/fundraisers')

    from src.students import bp as students_bp
    app.register_blueprint(blueprint=students_bp, url_prefix='/students')

    from src.transactions import bp as transactions_bp
    app.register_blueprint(blueprint=transactions_bp, url_prefix='/transactions')

    from src.main import bp as main_bp
    app.register_blueprint(blueprint=main_bp, url_prefix='')

    return app
