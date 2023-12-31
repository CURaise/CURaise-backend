from flask import request

from src.main import bp
from src.utils import success_message


@bp.route('/', methods=['GET'])
def index():
    """
    The index page
    """

    return success_message('CURaise Backend. Please go to https://github.com/CURaise/CURaise-backend for more guidance')
