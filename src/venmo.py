import os
from dotenv import load_dotenv
from venmo_api import Client

load_dotenv()

client = Client(access_token=os.environ["VENMO_TOKEN"])


def get_user_id(username):
    user = client.user.search_for_users(query=username)
    return user[0].id


def get_user_transactions(user_id):
    transactions = client.user.get_user_transactions(user_id=user_id)
    return transactions


if __name__ == "__main__":
    id = get_user_id("stevenyuser")
    transactions = get_user_transactions(id)
    for transaction in transactions:
        print(transaction)
