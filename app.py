from flask import Flask
from routes.auth import auth
from routes.admin import admin
from routes.user import user

app = Flask(__name__)
app.secret_key = "abc123"

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

app.run(debug=True)
