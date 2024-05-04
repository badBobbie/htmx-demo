from __future__ import annotations


def merge_users_with_roles(users: list, roles: list) -> list:
    for user in users:
        role_id = user["role"]
        user["role"] = [role for role in roles if role["id"] == role_id][0]

    return users


def merge_user_with_role(user: dict, roles: list) -> dict:
    role_id = user["role"]
    user["role"] = [role for role in roles if role["id"] == role_id][0]

    return user


def get_user_by_id(user_id: int, user_list: list) -> tuple[dict, int] | tuple[None, None]:
    for index, user in enumerate(user_list):
        if int(user_id) == int(user["id"]):
            return user, index

    return None, None


def get_user_by_user_name(user_name: str, user_list: list) -> dict | None:
    for user in user_list:
        if user_name == user["user_name"]:
            return user

    return None
