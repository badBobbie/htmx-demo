from __main__ import app

from flask import redirect, render_template, request, make_response

from services.json_service import *
from services.user_service import *


@app.route("/user/list")
def get_user_list():
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user_list = merge_users_with_roles(users_data["data"], roles_data["data"])

    return render_template("components/user-list.html", users=user_list, roles=roles_data["data"])


@app.route("/user/search")
def get_user_search():
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    request_user_name = request.args.get("user_name")
    user_list = list()

    if not request_user_name:
        return redirect("/user/list")

    user = get_user_by_user_name(request_user_name, users_data["data"])

    if user:
        user_list.append(merge_user_with_role(user, roles_data["data"]))

    return render_template("components/user-list.html", users=user_list)


@app.route("/user/<user_id>")
def get_user(user_id: int):
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user, index = get_user_by_id(user_id, users_data["data"])

    if user:
        user = merge_user_with_role(user, roles_data["data"])

    return render_template("components/user-list-item.html", user=user)


@app.route("/user/create", methods=["POST"])
def post_user_create():
    users_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")
    user = {
        "id": len(users_data["data"]) + 1,
        "user_name": request.form["user_name"],
        "login": request.form["login"],
        "password": request.form["password"],
        "role": int(request.form["role"])
    }

    users_data["data"].append(user)
    write_to_json("data/users.json", users_data)

    user = merge_user_with_role(user, roles_data["data"])

    return render_template("components/user-list-item.html", user=user)


@app.route("/user/<user_id>", methods=["PUT"])
def put_user_update(user_id: int):
    user_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user, user_index = get_user_by_id(user_id, user_data["data"])

    user["user_name"] = request.form["user_name"]
    user["passsword"] = request.form["password"]
    user["role"] = int(request.form["role"])

    user_data["data"][user_index] = user

    write_to_json("data/users.json", user_data)

    user = merge_user_with_role(user, roles_data["data"])

    return render_template("components/user-list-item.html", user=user)


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    users_data = read_from_json("data/users.json")

    user, index = get_user_by_id(user_id, users_data["data"])

    users_data["data"].pop(index)
    write_to_json("data/users.json", users_data)

    response = make_response()
    response.headers["HX-Trigger"] = "User was deleted"

    return response, 200


@app.route("/user/form/update/<user_id>")
def get_user_form_update(user_id: int):
    user_data = read_from_json("data/users.json")
    roles_data = read_from_json("data/roles.json")

    user, user_index = get_user_by_id(user_id, user_data["data"])
    if user is not None:
        user = merge_user_with_role(user, roles_data["data"])
        return render_template("components/user-form.html", user=user, roles=roles_data["data"])
    else:
        return '', 404


@app.route("/user/form/create")
def get_user_form_create():
    roles_data = read_from_json("data/roles.json")

    return render_template("components/user-form.html", roles=roles_data["data"])
