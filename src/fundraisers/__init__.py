from flask import Blueprint

bp = Blueprint('fundraisers', __name__)

from src.fundraisers import routes
