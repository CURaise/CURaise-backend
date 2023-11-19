from flask import Blueprint

from students import routes

bp = Blueprint('transactions', __name__)
