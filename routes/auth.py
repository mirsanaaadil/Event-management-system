from flask import Blueprint, render_template, request , redirect, session
import sqlite3
auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connet("database.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user=cur.fetchone()

        if user:
            session["role"] = user[3]
            if user[3] == "admin":
                return redirect("/admin")
            else:
                return redirect("/user")
        else:
            return render_template("login.html", msg="Wrong username or password")
    return render_template("login.html")

                    