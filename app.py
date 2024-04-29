from flask import Flask, render_template, request

from services.json_service import *
from services.data_service import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    users_data = read_from_json("data/users.json")
    permission_list_data = read_from_json("data/permissions.json")
    user_list = merge_users_with_permissions(users_data["data"], permission_list_data["data"])

    return render_template("user-list.html", users=user_list)


@app.route("/permissions")
def permissions():
    permission_list_data = read_from_json("data/permissions.json")

    return render_template("permission-list.html", permissions=permission_list_data["data"])


@app.route("/create", methods=["POST"])
def create_user():
    users_data = read_from_json("data/users.json")
    permission_list_data = read_from_json("data/permissions.json")
    users_data["data"].append({
        "id": len(users_data["data"]) + 1,
        "nick_name": request.form["nick_name"],
        "roles": request.form["roles"]
    })

    write_to_json("data/users.json", users_data)

    user_list = merge_users_with_permissions(users_data["data"], permission_list_data["data"])

    return render_template("users.html", users=user_list)
