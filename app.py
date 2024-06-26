from flask import Flask

app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from routes.user_routes import *
from routes.roles_routes import *
from routes.app_routes import *
from routes.error_routes import *

if __name__ == "__main__":
    app.run(debug=True)
