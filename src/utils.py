import json
from functools import wraps
from flask_login import current_user

DATETIME_FORMAT = "%Y-%m-%d'T'%H:%M:%S"

class FAIL_MSG:
    class POST_FORM:
        ERROR = "You submitted a form that contains misrepresented values. "
        FIELD_NAME_WRONG = "Please double check the submission field has everything contained or the name is correct. "

    class PARSE_ERROR:
        BOOLEAN = "Unable to parse the boolean supplied. Should be either True or False. "
        DATETIME = "Unable to parse the datetime supplied. "
        FLOAT = "Unable to parse the float supplied. "

    class VENMO:
        UNABLE_GET_USER_ID = "Unable to get the user id by the username provided. "
        UNABLE_GET_TRANSACTION = "Unable to get the transactions by the id provided. "
        TIMEOUT = "Timed out when trying to query venmo. "

    ADD_TO_DATABASE = "Internal issue. Unable to add the item to the database. "
    REMOVE_FROM_DATABASE = "Internal issue. Unable to remove the item from the database. "
    TARGET_NOT_FOUND = "Target not found in our database. Unable to query. "

    LOGIN_REQUIRED = "Login required. "
    SIGNUP_FAILED = "Sign up failed for unknown reasons. "
    LOGIN_FAILED = "Login Failed for unknown reasons. "
    SIGNOUT_FAILED = "Sign out Failed for unknown reasons. "
    WRONG_PASSWORD = "Wrong password. "


def success_message(x, code=201):
    """
    The success message.
    :param x: Message to be returned. In dict
    :param code: code to be returned. Default 201
    :return: (json.dumps(x), code)
    """
    if hasattr(x, 'serialize'):
        x = x.serialize(ios_style=True)
    return json.dumps({'status': 'success', 'success_msg': x}), code


def failure_message(x, code=400):
    """
    The failure message.
    :param x: Message to be returned. In STRING
    :param code: code to be returned. Default 400
    :return: (json.dumps(x), code)
    """
    return json.dumps({'status': 'error', 'error_msg': x}), code


def role_required(role):
    """
    A decorator function that is used for differentiated access (because there are two roles: students and clubs)
    NOTE: admin can bypass all roles.
    :param role: student or club
    :return: the decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # print(current_user.authenticated)
            if not current_user.is_authenticated or (current_user.role != role and current_user.role != 'admin'):
                return failure_message(FAIL_MSG.LOGIN_REQUIRED)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
