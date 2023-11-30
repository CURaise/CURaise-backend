from src.main import bp
from src.utils import success_message


@bp.route('/', methods=['GET'])
def index():
    return success_message('CURaise Backend. Please go to https://github.com/CURaise/CURaise-backend for more guidance')


@bp.route('/signup/', methods=['POST'])
def signup():
    pass


@bp.route('/signin/', methods=['POST'])
def signin():
    pass
