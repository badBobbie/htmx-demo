from __main__ import app
from flask import redirect, url_for, render_template, request

from services.json_service import *
from services.data_service import *


@app.route("/user/list")
def users():
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user_list = merge_users_with_roles(users_data["data"], roles_data["data"])

    return render_template("user-list.html", users=user_list)


@app.route("/user/search")
def user_search():
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    request_user_name = request.args.get("user_name")
    user_list = list()

    if request_user_name:
        user = get_user_by_user_name(request_user_name, users_data["data"])

        if user:
            user_list.append(merge_user_with_role(user, roles_data["data"]))

        return render_template("user-list.html", users=user_list)
    else:
        return redirect(url_for("users"))


@app.route("/user/form/update/<user_id>")
def get_user_form_update(user_id: int):
    user_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user, user_index = get_user_by_id(user_id, user_data["data"])
    if user is not None:
        user = merge_user_with_role(user, roles_data["data"])
        return render_template("update-user-form.html", user=user, roles=roles_data["data"])
    else:
        return


@app.route("/user/create", methods=["POST"])
def create_user():
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")
    users_data["data"].append({
        "id": len(users_data["data"]) + 1,
        "user_name": request.form["user_name"],
        "permission": request.form["permission"]
    })

    write_to_json("data/users.json", users_data)

    user_list = merge_users_with_roles(users_data["data"], roles_data["data"])

    return render_template("user-list.html", users=user_list)


@app.route("/user/<user_id>", methods=["PUT"])
def update_user_form(user_id: int):
    user_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user, user_index = get_user_by_id(user_id, user_data["data"])

    user["user_name"] = request.form["user_name"]
    user["permission"] = int(request.form["permission"])

    user_data["data"][user_index] = user

    write_to_json("data/users.json", user_data)

    user = merge_user_with_role(user, roles_data["data"])

    return render_template("user-list-item.html", user=user)
