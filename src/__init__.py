from flask import Flask

from config import Config
from models import db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


config = Config()

app = create_app(config)
