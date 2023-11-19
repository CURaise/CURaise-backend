import json


def success_message(x, code=201):
    return json.dumps(x), code


def failure_message(x, code=400):
    return json.dumps(x), code
