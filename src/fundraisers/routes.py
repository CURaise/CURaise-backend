from fundraisers import bp
from models import Club, Fundraiser
from extensions import db
from src.utils import *
from datetime import datetime


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

