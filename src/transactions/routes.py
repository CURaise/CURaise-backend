import random
import string

from src.extensions import db
from src.transactions import bp
from src.models import Club, Fundraiser, FundraiserItem
from src.utils import *


@bp.route('/verify/', methods=['POST'])


@bp.route('/create/', methods=['POST'])
def create_transaction():
    pass


def get_qr_code_link(transaction_id, reference_string):
    return f'https://chart.googleapis.com/chart?cht=qr&chl={transaction_id}__{reference_string}&chs=500x500'


def create_reference_string(transaction_id):
    transaction_id * 76622729181571704961
    characters = string.ascii_letters + string.digits
    random_string = [''.join(random.choice(characters)) for _ in range(15)]
    return random_string
