from flask import Blueprint

bp = Blueprint('posts', __name__)

from src.clubs import routes
