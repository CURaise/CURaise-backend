from flask import request

import json

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class FAIL_MSG:
    class POST_FORM:
        ERROR = "You submitted a form that contains misrepresented values. "
        FIELD_NAME_WRONG = "Please double check the submission field has everything contained or the name is correct. "

    class PARSE_ERROR:
        BOOLEAN = "Unable to parse the boolean supplied. Should be either True or False. "
        DATETIME = "Unable to parse the datetime supplied. "
        FLOAT = "Unable to parse the float supplied. "

    ADD_TO_DATABASE = "Internal issue. Unable to add the item to the database. "
    REMOVE_FROM_DATABASE = "Internal issue. Unable to remove the item from the database. "
    TARGET_NOT_FOUND = "Target not found in our database. Unable to query. "


def success_message(x, code=201):
    """
    The success message.
    :param x: Message to be returned. In dict
    :param code: code to be returned. Default 201
    :return: (json.dumps(x), code)
    """
    if hasattr(x, 'serialize'):
        x = x.serialize()
    return json.dumps({'status': 'success', 'success_msg': x}), code


def failure_message(x, code=400):
    """
    The failure message.
    :param x: Message to be returned. In STRING
    :param code: code to be returned. Default 400
    :return: (json.dumps(x), code)
    """
    return json.dumps({'status': 'error', 'error_msg': x}), code
