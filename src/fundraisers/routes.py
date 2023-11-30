from datetime import datetime

from src.extensions import db
from src.fundraisers import bp
from src.models import Club, Fundraiser, FundraiserItem
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


@bp.route('/<fundraiser_id>/', methods=['GET'])
def get_by_fundraiser_id(fundraiser_id):
    fundraiser = Fundraiser.query.filter_by(id=fundraiser_id).first()

    if fundraiser is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND + "Target=fundraiser.")

    return success_message(fundraiser)


@bp.route('/club/<club_id>/', methods=['GET'])
def get_by_club_id(club_id):
    fundraisers_by_club = [fundraiser.serialize() for fundraiser in Fundraiser.query.filter_by(club_id=club_id)]

    return success_message(fundraisers_by_club)


@bp.route('/', methods=['GET'])
def get_all_fundraisers():
    all_fundraisers = [fundraiser.serialize() for fundraiser in Fundraiser.query.all()]

    return all_fundraisers


@bp.route('/<fundraiser_id>/edit/', methods=['PUT'])
def edit_fundraiser(fundraiser_id):
    try:
        json_data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    fundraiser = Fundraiser.query.filter_by(id=fundraiser_id).first()

    if fundraiser is None:
        return failure_message(FAIL_MSG.TARGET_NOT_FOUND)

    for k in json_data.keys():
        if not hasattr(fundraiser, k):
            return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG)

    for k, v in json_data.items():
        setattr(fundraiser, k, v)

    try:
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(fundraiser)


@bp.route('/add_item/', methods=['POST'])
def add_fundraiser_item():
    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        price = float(json_data['price'])
        description = json_data['description']
        fundraiser_id = json_data['fundraiser_id']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))
    except ValueError as e:
        return failure_message(FAIL_MSG.PARSE_ERROR.FLOAT + str(e))

    new_fundraiser_item = FundraiserItem(
        name=name,
        price=price,
        description=description,
        fundraiser=fundraiser_id
    )

    try:
        db.session.add(new_fundraiser_item)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(new_fundraiser_item)


@bp.route('/<fundraiser_id>/', methods=['DELETE'])
def delete_fundraiser_by_id(fundraiser_id):
    fundraiser = get_by_fundraiser_id(fundraiser_id=fundraiser_id)

    # If and only if the return is tuple, the error was prompted in the getting function
    if isinstance(fundraiser, tuple):
        return fundraiser

    try:
        db.session.delete(fundraiser)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.REMOVE_FROM_DATABASE + str(e))

    return success_message(fundraiser)
