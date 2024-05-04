from __main__ import app
from flask import redirect, url_for, render_template, request

from services.json_service import *
from services.data_service import *


@app.route("/role/list")
def permissions():
    roles_data = read_from_json("data/roles.json")

    return render_template("role-list.html", roles=roles_data["data"])