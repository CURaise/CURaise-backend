from flask import Flask

from config import Config

def main(config):
    app = Flask(__name__)
    app.config.from_object(config)

    return app

