from __main__ import app

from flask import redirect, render_template, request, make_response

from services.json_service import *
from services.role_service import *
from services.user_service import *


@app.route("/role/list")
def get_role_list():
    roles_data = read_from_json("data/roles.json")

    return render_template("components/role-list.html", roles=roles_data["data"], route="/roles")


@app.route("/role/search")
def get_role_search():
    roles_data = read_from_json("data/roles.json")

    request_role_title = request.args.get("role-title")
    role_list = list()

    if not request_role_title:
        return redirect("/role/list")

    role = get_role_by_title(request_role_title, roles_data["data"])

    if role:
        role_list.append(role)

    return render_template("components/role-list.html", roles=role_list)


@app.route("/role/<role_id>")
def get_role(role_id: int):
    role_data = read_from_json("data/roles.json")

    role, role_id = get_role_by_id(role_id, role_data["data"])

    return render_template("components/role-list-item.html", role=role)


@app.route("/role/create", methods=["POST"])
def post_role_create():
    role_data = read_from_json("data/roles.json")
    role = {
        "id": len(role_data["data"]) + 1,
        "title": request.form.get("title"),
        "description": request.form.get("description"),
    }

    role_data["data"].append(role)
    write_to_json("data/roles.json", role_data)

    return render_template("components/role-list-item.html", role=role)


@app.route("/role/<role_id>", methods=["PUT"])
def put_update_role(role_id: int):
    role_data = read_from_json("data/roles.json")

    role, role_index = get_role_by_id(role_id, role_data["data"])

    role["title"] = request.form["title"]
    role["description"] = request.form["description"]

    role_data["data"][role_index] = role

    write_to_json("data/roles.json", role_data)

    return render_template("components/role-list-item.html", role=role)


@app.route("/role/<role_id>", methods=["DELETE"])
def delete_role(role_id: int):
    role_data = read_from_json("data/roles.json")
    user_data = read_from_json("data/users.json")

    role, role_index = get_role_by_id(role_id, role_data["data"])
    indexes = get_users_indexes_by_role_id(role_id, user_data["data"])

    for index in indexes:
        if len(role_data["data"]):
            user_data["data"][index]["role"] = role_data["data"][0]["id"]
        else:
            user_data["data"][index]["role"] = 0

    role_data["data"].pop(role_index)

    write_to_json("data/roles.json", role_data)
    write_to_json("data/users.json", user_data)

    response = make_response()
    response.headers["HX-Trigger"] = "Role was deleted"

    return response, 200


@app.route("/role/form/update/<role_id>")
def get_role_form_update(role_id: int):
    role_data = read_from_json("data/roles.json")

    role, role_index = get_role_by_id(role_id, role_data["data"])

    if role is not None:
        return render_template("components/role-form.html", role=role)

    return '', 404


@app.route("/role/form/create")
def get_role_form_create():
    return render_template("components/role-form.html")
