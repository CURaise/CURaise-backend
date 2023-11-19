from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .club import Club
from .fundraiser import Fundraiser

