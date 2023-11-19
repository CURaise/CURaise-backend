from flask import Blueprint

bp = Blueprint('fundraisers', __name__)

from fundraisers import routes
