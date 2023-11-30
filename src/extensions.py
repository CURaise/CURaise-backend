from flask_sqlalchemy import SQLAlchemy
from venmo_api import Client
from flask_login import LoginManager

import os

db = SQLAlchemy()
client = Client(access_token=os.environ["VENMO_TOKEN"], )
login_manager = LoginManager()
