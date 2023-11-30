import random
import string

from src.extensions import db
from src.extensions import client
from src.transactions import bp
from src.models import Club, Fundraiser, FundraiserItem
from src.utils import *


@bp.route('/verify/', methods=['POST'])
def verify_transaction():
    try:
        json_data = json.loads(request.data)
        username = json_data['username']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    try:
        user_id = client.user.search_for_users(query=username)[0].id
    except Exception as e:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_USER_ID + str(e))

    try:
        new_transactions = client.user.get_user_transactions(user_id=user_id)
    except Exception as e:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_TRANSACTION + str(e))

    return success_message(new_transactions)


@bp.route('/create/', methods=['POST'])
def create_transaction():
    pass


# def get_qr_code_link(transaction_id, reference_string):
#     return f'https://chart.googleapis.com/chart?cht=qr&chl={transaction_id}__{reference_string}&chs=500x500'
#
#
# def create_reference_string(transaction_id):
#     transaction_id * 76622729181571704961
#     characters = string.ascii_letters + string.digits
#     random_string = [''.join(random.choice(characters)) for _ in range(15)]
#     return random_string
