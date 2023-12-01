from flask import request

from src.services import bp
from src.utils import success_message


@bp.route('/signup/', methods=['POST'])
def signup():
    pass


@bp.route('/signin/', methods=['POST'])
def signin():
    pass
