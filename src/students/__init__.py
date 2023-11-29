from flask import Blueprint

bp = Blueprint('students', __name__)

from src.students import routes
