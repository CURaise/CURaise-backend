from src.clubs import bp
from src.extensions import db
from src.models import Club
from src.utils import *


@bp.route('/signup/', methods=['POST'])
def create_club():
    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        description = json_data['description']
        venmo_username = json_data['venmo_username']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    try:
        new_club = Club(
            name=name,
            description=description,
            venmo_username=venmo_username
        )
        db.session.add(new_club)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(new_club.id)


@bp.route('/<club_id>/', methods=['GET'])
def get_club_by_id(club_id):
    target = Club.query.filter_by(id=club_id).first()

    if target is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + "Target=club.")

    return success_message(target.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/<club_id>/edit/', methods=['PUT'])
def edit_club(club_id):
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
        return failure_message(FAIL_MSG.ADD_TO_DATABASE)

    return success_message(club)


@bp.route('/<club_id>/', methods=['DELETE'])
def delete_by_club_id(club_id):
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
