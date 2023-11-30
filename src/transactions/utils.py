from src.extensions import client


def get_user_by_username(username: str):
    user_id = client.user.search_for_users(query=username, username=True)
