from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


from routes.user_routes import *
from routes.roles_routes import *

if __name__ == "__main__":
    app.run(debug=True)
