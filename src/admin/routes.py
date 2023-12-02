from flask import request
import asyncio

from src.admin import bp
from src.extensions import db
from src.models import Admin
from src.utils import *

from src.transactions.utils import get_user_by_username

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@bp.route('/signup/', methods=['POST'])
def create_admin():
    """
    Creates an admin user
    """

    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        email = json_data['email']
        password = json_data['password']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    password = generate_password_hash(password)
    try:
        new_admin = Admin(
            name=name,
            email=email,
            password=password
        )
        db.session.add(new_admin)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    login_user(new_admin, remember=True)

    return success_message(new_admin.id)


@bp.route('/signin/', methods=['POST'])
def signin_admin():
    """
    Signs in an admin user
    """

    try:
        json_data = json.loads(request.data)
        email = json_data['email']
        password = json_data['password']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    admin = Admin.query.filter_by(email=email).first()
    if admin is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND)

    if not check_password_hash(admin.password, password):
        return failure_message(FAIL_MSG.WRONG_PASSWORD)

    if login_user(admin, remember=True):
        return success_message("Log in success. ")
    else:
        return failure_message(FAIL_MSG.LOGIN_FAILED)


@bp.route('/signout/', methods=['POST'])
@role_required('admin')
def signout_admin():
    """
    Signs out an admin user
    """

    if logout_user():
        return success_message("Log out success. ")
    else:
        return failure_message(FAIL_MSG.SIGNOUT_FAILED)


@bp.route('/my/', methods=['GET'])
@role_required('admin')
def get_me():
    """
    Returns the current user
    """

    return success_message(current_user.serialize())


@bp.route('/my/edit/', methods=['PUT'])
@role_required('admin')
def edit_me():
    """
    Edits the current user
    """

    try:
        json_data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    for k in json_data.keys():
        if not hasattr(current_user, k):
            return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG)

    for k, v in json_data.items():
        setattr(current_user, k, v)

    try:
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(current_user.serialize())


@bp.route('/my/', methods=['DELETE'])
@role_required('admin')
def delete_me():
    """
    Deletes the current user
    """

    try:
        db.session.delete(current_user)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(current_user.serialize())
