from clubs import bp
from models import Club, Fundraiser
from extensions import db
from src.utils import *
from datetime import datetime


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
    try:
        target = Club.query.filter_by(id=club_id).first()
    except Exception as e:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + str(e))

    return success_message(target.serialize(exclude_venmo_username=True, simplified=True))


@bp.route('/add_members/', methods=['POST'])
def add_members():
    pass
