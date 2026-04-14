from flask import Flask
from routes.auth import auth
from routes.admin import admin
from routes.user import user
from routes.executive import executive


app = Flask(__name__)
app.secret_key = "abc123"

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(executive)

app.run(debug=True)
