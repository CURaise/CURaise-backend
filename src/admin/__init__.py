from flask import Blueprint

bp = Blueprint('admin', __name__)

from src.admin import routes
