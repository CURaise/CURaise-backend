from src.extensions import client
import asyncio


async def get_user_by_username(nickname: str, username: str) -> (int, object):
    """
    Get a user by its nickname and username
    :param nickname: the nickname on the venmo account
    :param username: the username on the venmo account
    :return: (status_code: 0 means ok, -1 means empty, -2 means timeout), (user object)
    """
    async def async_get_user_by_username():
        users = client.user.search_for_users(query=nickname, limit=5)
        for user in users:
            if user.username == username:
                return user
        return None

    # We need to use asyncio because it's very easy to take a long time to query. We do not want that to happen.
    try:
        users = await asyncio.wait_for(async_get_user_by_username(), timeout=2)
    except asyncio.TimeoutError:
        print("Timed out when getting the user!")
        return -2, None

    for u in users:
        if u.username == username:
            return 0, u

    return -1, None


async def get_transaction(buyer_id: int, club_id: int) -> (int, list):
    """
    Get the transaction between a buyer and a club
    :param buyer_id: the venmo id of the buyer
    :param club_id: the venmo id of the club
    :return:
    """
    async def async_get_transaction():
        return client.user.get_transaction_between_two_users(user_id_one=buyer_id, user_id_two=club_id)

    # We need to use asyncio because it's very easy to take a long time to query. We do not want that to happen.
    try:
        transactions = await asyncio.wait_for(async_get_transaction(), timeout=2)
    except asyncio.TimeoutError:
        print("Timed out when getting the user!")
        return -2, None

    return 0, transactions
