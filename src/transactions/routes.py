from flask import request, redirect
import asyncio
from src.extensions import db
from src.extensions import client
from src.transactions import bp
from src.models import Club, Fundraiser, FundraiserItem
from src.utils import *
from src.transactions.utils import *


@bp.route('/verify/', methods=['POST'])
def verify_transaction():
    """
    Verify if a transaction is made
    :return: success if the transaction is made. Unsuccessful if not. Success returns the transaction_id and amount paid
    """
    try:
        json_data = json.loads(request.data)
        buyer_venmo_id = json_data['buyer_venmo_id']
        club_venmo_id = json_data['club_venmo_id']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    try:
        status, tran = asyncio.run(get_transaction(buyer_id=buyer_venmo_id, club_id=club_venmo_id))
    except Exception as e:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_TRANSACTION + str(e))

    if status == -2:
        return failure_message(FAIL_MSG.VENMO.TIMEOUT)
    if status == -1:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_TRANSACTION)

    amount = 0.0 if tran.amount is None else tran.amount

    return success_message({'transaction_id': tran.payment_id, 'amount': amount})


@bp.route('/qrcode/', methods=['POST'])
def create_qrcode():
    try:
        json_data = json.loads(request.data)
        transaction_id = json_data['transaction_id']
    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    return redirect(get_qr_code_link(transaction_id))

# @bp.route('/create/', methods=['POST'])
# def create_transaction():
#     try:
#         json_data = json.loads(request.data)
#         transaction_id = json_data['transaction_id']
#     except KeyError as e:
#         return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
#     except json.decoder.JSONDecodeError as e:
#         return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))
