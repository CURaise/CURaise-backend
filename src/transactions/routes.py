from flask import request
import asyncio

import random
import string

from src.extensions import db
from src.extensions import client
from src.transactions import bp
from src.models import Club, Fundraiser, FundraiserItem
from src.utils import *
from src.transactions.utils import *


@bp.route('/verify/', methods=['POST'])
def verify_transaction():
    try:
        json_data = json.loads(request.data)
        buyer_venmo_id = json_data['buyer_venmo_id']
        club_venmo_id = json_data['club_venmo_id']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    status, amount = asyncio.run(get_transaction(buyer_id=buyer_venmo_id, club_id=club_venmo_id))

    if status == -2:
        return failure_message(FAIL_MSG.VENMO.TIMEOUT)
    if status == -1:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_TRANSACTION)

    amount = 0.0 if amount is None else amount

    return success_message(amount)


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
