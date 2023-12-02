from flask import request
import asyncio

from src.clubs import bp
from src.extensions import db
from src.models import Club
from src.utils import *

from src.transactions.utils import get_user_by_username

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@DeprecationWarning
# @bp.before_request
def check_login():
    public_endpoints = ['signup']
    if request.endpoint in public_endpoints:
        return  # If nothing returned, skip
    return failure_message(FAIL_MSG.LOGIN_REQUIRED)


@bp.route('/signup/', methods=['POST'])
def create_club():
    '''
    Creates a club
    '''

    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        description = json_data['description']
        venmo_username = json_data['venmo_username']

        email = json_data['email']
        password = json_data['password']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    status, venmo_user = asyncio.run(get_user_by_username(username=venmo_username))

    if status == -2:
        return failure_message(FAIL_MSG.VENMO.TIMEOUT + 'create_club')
    if status == -1:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_USER_ID + 'create_club')

    password = generate_password_hash(password)

    try:
        new_club = Club(
            name=name,
            description=description,
            venmo_id=venmo_user.id,
            venmo_username=venmo_username,
            email=email,
            password=password
        )
        db.session.add(new_club)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    login_user(new_club, remember=True)

    return success_message(new_club.id)


@bp.route('/signin/', methods=['POST'])
def signin_club():
    '''
    Signs into a club
    '''

    try:
        json_data = json.loads(request.data)
        email = json_data['email']
        password = json_data['password']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    club = Club.query.filter_by(email=email).first()
    if club is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND)

    if not check_password_hash(club.password, password):
        return failure_message(FAIL_MSG.WRONG_PASSWORD)

    if login_user(club, remember=True):
        return success_message("Log in success. ")
    else:
        return failure_message(FAIL_MSG.LOGIN_FAILED)


@bp.route('/signout/', methods=['POST'])
@role_required('club')
def signout_club():
    '''
    Signs out of a club
    '''

    if logout_user():
        return success_message("Log out success. ")
    else:
        return failure_message(FAIL_MSG.SIGNOUT_FAILED)


@bp.route('/my/', methods=['GET'])
@role_required('club')
def get_me():
    '''
    Returns the club user
    '''

    return success_message(current_user.serialize())


@bp.route('/my/edit/', methods=['PUT'])
@role_required('club')
def edit_me():
    '''
    Edits the club user
    '''

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
@role_required('club')
def delete_me():
    '''
    Deletes the club user
    '''

    try:
        db.session.delete(current_user)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(current_user.serialize())


@bp.route('/<club_id>/', methods=['GET'])
@role_required('admin')
def get_club_by_id(club_id):
    '''
    Gets a club by its id
    '''

    target = Club.query.filter_by(id=club_id).first()

    if target is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + "Target=club.")

    return success_message(target.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/<club_id>/edit/', methods=['PUT'])
@role_required('admin')
def edit_club(club_id):
    '''
    Edits the club by its id
    '''

    try:
        json_data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    club = Club.query.filter_by(id=club_id).first()

    if club is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND)

    for k in json_data.keys():
        if not hasattr(club, k):
            return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG)

    for k, v in json_data.items():
        setattr(club, k, v)

    try:
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(club)


@bp.route('/<club_id>/', methods=['DELETE'])
@role_required('admin')
def delete_by_club_id(club_id):
    '''
    Deletes the club by its id
    '''

    club = get_club_by_id(club_id=club_id)

    # If and only if the return is tuple, the error was prompted in the getting function
    if isinstance(club, tuple):
        return club

    try:
        db.session.delete(club)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(club)
