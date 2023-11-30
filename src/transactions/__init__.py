from flask import Blueprint

bp = Blueprint('transactions', __name__)

from src.transactions import routes
