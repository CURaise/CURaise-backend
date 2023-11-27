from flask import Flask

from config import Config
from extensions import db

# Imports for creating the tables. DO NOT remove them for import optimization...
from models.club import Club
from models.fundraiser import Fundraiser
from models.fundraiser_item import FundraiserItem
from models.student import Student
from models.transaction import Transaction


def create_app(config=Config()):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from clubs import bp as clubs_bp
    app.register_blueprint(blueprint=clubs_bp, url_prefix='/clubs')

    from fundraisers import bp as fundraisers_bp
    app.register_blueprint(blueprint=fundraisers_bp, url_prefix='/fundraisers')

    from students import bp as students_bp
    app.register_blueprint(blueprint=students_bp, url_prefix='/students')

    from transactions import bp as transactions_bp
    app.register_blueprint(blueprint=transactions_bp, url_prefix='/transactions')

    from main import bp as main_bp
    app.register_blueprint(blueprint=main_bp, url_prefix='')

    return app
