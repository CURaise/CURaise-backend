from flask_sqlalchemy import SQLAlchemy

from .club import Club
from .fundraiser import Fundraiser
from .fundraiser_item import FundraiserItem
from .student import Student
from .transaction import Transaction

db = SQLAlchemy()
