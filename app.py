from flask import Flask
from routes.auth import auth


app = Flask(__name__)
app.secret_key = "abc123"

app.register_blueprint(auth)


app.run(debug=True)
