from flask import Blueprint

from src.students import routes

bp = Blueprint('transactions', __name__)
