from flask import Blueprint

bp = Blueprint('services', __name__)

from src.services import routes
