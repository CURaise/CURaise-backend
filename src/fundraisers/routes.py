from datetime import datetime

from extensions import db
from fundraisers import bp
from models import Club, Fundraiser
from src.utils import *


@bp.route('/create/', methods=['POST'])
def create_fundraisers():
    """
    Add a fundraiser event to the database.
    NOTE:
    active_status has to be either True or False
    start_datetime and start_datetime have to be in UTC parce-able DateTime format.
    :return: either success or failure message in json.
    """

    try:
        json_data = json.loads(request.data)
        club_id = json_data['club_id']
        title = json_data['title']
        description = json_data['description']
        # active_status = eval(json_data['active_status'].lower().capitalize())
        active_status = json_data['active_status']
        start_datetime = datetime.strptime(json_data['start_datetime'], DATETIME_FORMAT)
        end_datetime = datetime.strptime(json_data['end_datetime'], DATETIME_FORMAT)
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))
    # except NameError as e:
    #     return failure_message(FAIL_MSG.PARSE_ERROR.BOOLEAN + str(e))
    except ValueError as e:
        return failure_message(FAIL_MSG.PARSE_ERROR.DATETIME + str(e))

    if Club.query.filter_by(id=club_id).first() is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + "Target=club")

    try:
        new_fundraiser = Fundraiser(
            club_id=club_id,
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


@bp.route('<fundraiser_id>/', methods=['GET'])
def get_by_fundraiser_id(fundraiser_id):
    fundraiser = Fundraiser.query.filter_by(id=fundraiser_id).first()

    if fundraiser is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + "Target=fundraiser.")

    return success_message(fundraiser)


@bp.route('club/<club_id>/', methods=['GET'])
def get_by_club_id(club_id):
    fundraisers_by_club = [fundraiser.serialize() for fundraiser in Fundraiser.query.filter_by(club_id=club_id)]

    return success_message(fundraisers_by_club)

