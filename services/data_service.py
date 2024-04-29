def merge_users_with_permissions(users: list, permissions: list) -> list:
    for user in users:
        for index, role_id in enumerate(user["permission_list"]):
            user["permission_list"][index] = [permission for permission in permissions if permission["id"] == role_id][0]

    return users
