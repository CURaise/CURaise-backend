import random
import string


def get_qr_code_link(transaction_id, reference_string):
    return f'https://chart.googleapis.com/chart?cht=qr&chl={transaction_id}__{reference_string}&chs=500x500'


def create_reference_string(transaction_id):
    transaction_id * 76622729181571704961
    characters = string.ascii_letters + string.digits
    random_string = [''.join(random.choice(characters)) for _ in range(15)]
    return random_string
