from flask import Blueprint

bp = Blueprint('clubs', __name__)

from src.clubs import routes
