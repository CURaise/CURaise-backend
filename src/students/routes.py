from src.clubs import bp
from src.extensions import db
from src.models import Student
from src.utils import *

from src.transactions.utils import get_user_by_username


@bp.route('/signup/', methods=['POST'])
def create_student():
    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        netid = json_data['netid']
        venmo_username = json_data['venmo_username']
        venmo_nickname = json_data['venmo_nickname']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    status, venmo_user = get_user_by_username(nickname=venmo_nickname, username=venmo_username)

    if status == -2:
        return failure_message(FAIL_MSG.VENMO.TIMEOUT + 'create_student')
    if status == -1:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_USER_ID + 'create_student')

    try:
        new_student = Student(
            name=name,
            netid=netid,
            venmo_id=venmo_user.id,
            venmo_nickname=venmo_nickname,
            venmo_username=venmo_username
        )
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(new_student.id)


@bp.route('/netid/<netid>/', methods=['GET'])
@bp.route('/<student_id>/', methods=['GET'])
def get_student_by_id(student_id=None, netid=None):
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
def edit_student_by_id(student_id=None, netid=None):
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

    return success_message(student)


@bp.route('/netid/<netid>/', methods=['DELETE'])
@bp.route('/<student_id>/', methods=['DELETE'])
def delete_student_by_id(student_id=None, netid=None):
    student = get_student_by_id(student_id=student_id, netid=netid)

    # If and only if the return is tuple, the error was prompted in the getting function
    if isinstance(student, tuple):
        return student

    try:
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(student)
