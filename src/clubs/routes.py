from clubs import bp
from models import Club, Fundraiser
from extensions import db
from src.utils import *


@bp.route('/signup/', methods=['POST'])
def create_club():
    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        description = json_data['description']
        venmo_username = json_data['venmo_username']
    except KeyError as e:
        return failure_message(FAIL_MSG.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM_ERROR + str(e))

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


@bp.route('/add_fundraisers/', methods=['POST'])
def add_fundraisers():
    try:
        json_data = json.loads(request.data)
        title = json_data['title']
        description = json_data['description']
        active_status = eval(json_data['active_status'])
        start_datetime = json_data['start_datetime']
        end_datetime = json_data['end_datetime']
    except KeyError as e:
        return failure_message(FAIL_MSG.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM_ERROR + str(e))
    except NameError as e:
        return failure_message(FAIL_MSG.POST_FORM_ERROR + str(e))

    try:
        new_fundraiser = Fundraiser(
            title=title,
            description=description,
            active_status=active_status,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
        db.session.add(new_fundraiser)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(new_fundraiser.id)


@bp.route('/add_members/', methods=['POST'])
def add_members():
    pass
