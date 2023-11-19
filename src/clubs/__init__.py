from flask import Blueprint

bp = Blueprint('clubs', __name__)

from clubs import routes
