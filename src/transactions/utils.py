from src.extensions import client
import asyncio

import random
import string


async def get_user_by_username(username: str) -> (int, object):
    """
    Get a user by its nickname and username
    :param nickname: the nickname on the venmo account
    :param username: the username on the venmo account
    :return: (status_code: 0 means ok, -1 means empty, -2 means timeout), (user object)
    """
    async def async_get_user_by_username():
        return client.user.get_user_by_username(username=username)
        # # DO NOT REMOVE THE COMMENTED CODE
        # users = client.user.search_for_users(query=nickname, limit=5)
        # for user in users:
        #     if user.username == username:
        #         return user
        # return None

    # We need to use asyncio because it's very easy to take a long time to query. We do not want that to happen.
    try:
        user = await asyncio.wait_for(async_get_user_by_username(), timeout=2)
    except asyncio.TimeoutError:
        print("Timed out when getting the user!")
        return -2, None

    return 0, user


async def get_transaction(buyer_id: int, club_id: int) -> (int, float):
    """
    Get the transaction between a buyer and a club
    :param buyer_id: the venmo id of the buyer
    :param club_id: the venmo id of the club
    :return: (status_code: 0 means ok, -1 means didn't get the transaction, -2 means time out), (transaction object)
    """
    async def async_get_transaction():
        return client.user.get_user_transactions(user_id=buyer_id, limit=10)

    # We need to use asyncio because it's very easy to take a long time to query. We do not want that to happen.
    try:
        transactions = await asyncio.wait_for(async_get_transaction(), timeout=2)
    except asyncio.TimeoutError:
        print("Timed out when getting the user!")
        return -2, None

    for tran in transactions:
        if tran.target.id == club_id:
            return 0, tran

    return -1, None


def create_reference_string(transaction_id):
    """
    Create a reference string that will be stored in the database.
    :param transaction_id: the transaction id
    :return: the reference string created
    """
    transaction_id * 76622729181571704961  # A large prime number
    characters = string.ascii_letters + string.digits
    random_string = [''.join(random.choice(characters)) for _ in range(15)]
    return ''.join(random_string)


def get_qr_code_link(transaction_id, reference_string):
    """
    Create the QR code
    :param transaction_id: the transaction id
    :param reference_string: the reference string based on the transaction id
    :return:
    """
    return f'https://chart.googleapis.com/chart?cht=qr&chl={transaction_id}__{reference_string}&chs=500x500'


