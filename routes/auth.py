from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Connect to database
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, username, password, role FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()

        if user:
            session["user_id"] = user[0]   # <-- store user_id in session
            session["role"] = user[3]      # <-- store role in session

            if user[3] == "admin":
                return redirect("/admin")
            else:
                return redirect("/user")
        else:
            return render_template("login.html", msg="Wrong username or password")

    return render_template("login.html")