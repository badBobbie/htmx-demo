from __future__ import annotations


def get_role_by_id(role_id: int, role_list: list) -> tuple[dict, int] | tuple[None, None]:
    for index, role in enumerate(role_list):
        if int(role["id"]) == int(role_id):
            return role, index

    return None, None


def get_role_by_title(role_name: str, role_list: list) -> dict | None:
    for role in role_list:
        if role["title"] == role_name:
            return role

    return None
