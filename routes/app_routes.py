from __main__ import app
from flask import redirect, render_template, request

from services.json_service import *


@app.route("/")
def index():
    return redirect("/users")


@app.route("/users")
def users():
    if not request.headers.get("HX-Request"):
        return render_template("index.html", route="/users")

    role_data = read_from_json("data/roles.json")

    return render_template("pages/users.html", roles=role_data["data"])


@app.route("/roles")
def roles():
    if not request.headers.get("HX-Request"):
        return render_template("index.html", route="/roles")

    return render_template("pages/roles.html")


@app.route("/websockets")
def websockets():
    if not request.headers.get("HX-Request"):
        return render_template("index.html", route="/websockets")

    return render_template("pages/websockets.html")