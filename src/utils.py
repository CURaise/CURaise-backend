import json


def success_message(x, code=201):
    """
    The success message.
    :param x: Message to be returned. In dict
    :param code: code to be returned. Default 201
    :return: (json.dumps(x), code)
    """
    return json.dumps(x), code


def failure_message(x, code=400):
    """
    The failure message.
    :param x: Message to be returned. In dict
    :param code: code to be returned. Default 400
    :return: (json.dumps(x), code)
    """
    return json.dumps(x), code
