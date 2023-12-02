from flask import request, redirect
import asyncio
from src.extensions import db
from src.extensions import client
from src.transactions import bp
from src.models import Transaction
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


@bp.route('/qrcode/<transaction_db_id>', methods=['GET'])
def create_qrcode(transaction_db_id):
    """
    Generate the QR code by the id of the transaction database provided. The app would query the reference string
    and incorporate it in the qrcode.
    :param transaction_db_id:
    :return:
    """
    try:
        reference_string = Transaction.query.filter_by(id=transaction_db_id).first().reference_string
    except Exception as e:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_TRANSACTION + str(e))
    return redirect(get_qr_code_link(transaction_db_id, reference_string=reference_string))


@bp.route('/create/', methods=['POST'])
def create_transaction():
    """
    Creates a transaction
    """

    try:
        json_data = json.loads(request.data)
        transaction_id = json_data['transaction_id']
        fundraiser_id = json_data['fundraiser_id']
        fundraiser_item_id = json_data['fundraiser_item_id']
        club_id = json_data['club_id']
        payer_id = json_data['payer_id']
        referrer = None
        if 'referrer' in json_data.keys():
            referrer = json_data['referrer']

    except KeyError as e:
        return failure_message(FAIL_MSG.POST_FORM.FIELD_NAME_WRONG + str(e))
    except json.decoder.JSONDecodeError as e:
        return failure_message(FAIL_MSG.POST_FORM.ERROR + str(e))

    reference_string = create_reference_string(transaction_id=transaction_id)

    try:
        status, tran = asyncio.run(get_transaction(buyer_id=payer_id, club_id=club_id))
    except Exception as e:
        return failure_message(FAIL_MSG.VENMO.UNABLE_GET_TRANSACTION + str(e))

    status_bool = (status == 0)

    try:
        new_tran = Transaction(
            reference_string=reference_string,
            fundraiser=fundraiser_id,
            item=fundraiser_item_id,
            club=club_id,
            payer=payer_id,
            status=status_bool,
            referrer=referrer,
        )
        db.session.add(new_tran)
        db.session.commit()
    except Exception as e:
        return failure_message(FAIL_MSG.ADD_TO_DATABASE + str(e))

    return success_message(new_tran)
