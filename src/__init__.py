from flask import Flask

from config import Config
from extensions import db


def create_app(config):
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

    return app


config = Config()

app = create_app(config)
