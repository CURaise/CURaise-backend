from flask import Blueprint

bp = Blueprint('students', __name__)

from students import routes
