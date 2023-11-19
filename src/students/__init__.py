from flask import Blueprint

from students import routes

bp = Blueprint('students', __name__)
