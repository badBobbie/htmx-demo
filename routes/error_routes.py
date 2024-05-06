from __main__ import app

from flask import render_template, request


@app.errorhandler(404)
def not_found(error):
    if not request.headers.get("HX-Request"):
        return render_template("index.html")

    return render_template("pages/error.html", error=error)
