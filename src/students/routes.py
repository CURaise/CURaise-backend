from flask import request

from src.students import bp
from src.extensions import db, auth
from src.models import Student
from src.utils import *

from src.transactions.utils import get_user_by_username

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user

import asyncio


@bp.route('/signup/', methods=['POST'])
def create_student():
    """
    Create a student
    :return: if success, the id of the student created
    """
    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        netid = json_data['netid']
        venmo_username = json_data['venmo_username']
        email = json_data['email']
        password = json_data['password']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    status, venmo_user = asyncio.run(get_user_by_username(username=venmo_username))

    if status == -2:
        return failure_message(FAIL_MSG.VENMO.TIMEOUT + 'create_student')
    if status == -1:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_USER_ID + 'create_student')

    # password = generate_password_hash(password)

    # Note: after user is created on firebase, it's possible it will not be populated in our database. FIXME
    user = auth.create_user(
        email=email,
        password=password
    )

    try:
        new_student = Student(
            name=name,
            netid=netid,
            venmo_id=venmo_user.id,
            venmo_username=venmo_username,
            email=email,
            password=password,
            firebase_uid=user.uid
        )
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    # # NOTE: STARTING DEC/3RD, AUTH MOVED TO FIREBASE, FLASK_LOGIN IS DEPRECATED FOR CLUB AND STUDENT, BUT CODE
    # # REMAINED FOR ORGANIZATIONAL PURPOSES.
    # login_user(new_student, remember=True)

    return success_message(user.uid)


@bp.route('/signin/', methods=['POST'])
def signin_student():
    """
    Signs in a student
    """

    try:
        json_data = json.loads(request.data)
        email = json_data['email']
        password = json_data['password']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    student = Student.query.filter_by(email=email).first()
    if student is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND)

    if not check_password_hash(student.password, password):
        return failure_message(FAIL_MSG.WRONG_PASSWORD)

    if login_user(student, remember=True):
        return success_message("Log in success. ")
    else:
        return failure_message(FAIL_MSG.LOGIN_FAILED)


@bp.route('/signout/', methods=['POST'])
@role_required('student')
def signout_student():
    """
    Signs out a student
    """

    if logout_user():
        return success_message("Success. ")
    else:
        return failure_message(FAIL_MSG.SIGNOUT_FAILED)


@bp.route('/my/', methods=['GET'])
# @role_required('student')
def get_me():
    """
    Returns the student user
    """

    authorization = request.args.get('Authorization').split('\n')[-1]

    uid = verify_firebase_token(authorization)
    if uid is None:
        return failure_message(FAIL_MSG.LOGIN_REQUIRED)

    user = firebase_get_model(uid)
    if user is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND)

    return success_message(user)
    # return success_message(current_user)


@bp.route('/my/edit/', methods=['PUT'])
@role_required('student')
def edit_me():
    """
    Edits the student user document
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

    return success_message(current_user.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/my/', methods=['DELETE'])
@role_required('student')
def delete_me():
    """
    Deletes the student user
    """

    try:
        db.session.delete(current_user)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(current_user.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/netid/<netid>/', methods=['GET'])
@bp.route('/<student_id>/', methods=['GET'])
@role_required('admin')
def get_student_by_id(student_id=None, netid=None):
    """
    Gets a student by its id
    """

    if (student_id is None and netid is None) or (student_id is not None and netid is not None):
        return failure_message(FAIL_MSG.POST_FORM.ERROR + 'student_id and netid should not be all supplied or none '
                                                          'applied')
    if student_id is not None:
        target = Student.query.filter_by(id=student_id).first()
    else:
        target = Student.query.filter_by(netid=netid).first()

    if target is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + "Target=student.")

    return success_message(target.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/netid/<netid>/edit', methods=['PUT'])
@bp.route('/<student_id>/edit', methods=['PUT'])
@role_required('admin')
def edit_student_by_id(student_id=None, netid=None):
    """
    Edits a student by its id
    """

    try:
        json_data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    student = get_student_by_id(student_id=student_id, netid=netid)

    for k in json_data.keys():
        if not hasattr(student, k):
            return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG)

    for k, v in json_data.items():
        setattr(student, k, v)

    try:
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(student.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/netid/<netid>/', methods=['DELETE'])
@bp.route('/<student_id>/', methods=['DELETE'])
@role_required('admin')
def delete_student_by_id(student_id=None, netid=None):
    """
    Deletes a student by its id
    """

    student = get_student_by_id(student_id=student_id, netid=netid)

    # If and only if the return is tuple, the error was prompted in the getting function
    if isinstance(student, tuple):
        return student

    try:
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(student.serialize(exclude_venmo_username=True, simplified=True))
