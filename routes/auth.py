from flask import Blueprint, render_template, request, redirect, session, flash
import sqlite3

auth = Blueprint("auth", __name__)



@auth.route("/", methods=["GET", "POST"])
def login():

    
    if "user_id" in session:
        if session["role"] == "admin":
            return redirect("/admin")
        elif session["role"] == "executive":
            return redirect("/executive")
        else:
            return redirect("/user")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""SELECT id, role, status FROM users WHERE email=? AND password=?""", (email, password))

        user = cur.fetchone()
        conn.close()

        if user:
            if user[1] == "user" and user[2] != "Approved":
                flash("Account not approved yet!")
                return redirect("/")

            
            session["user_id"] = user[0]
            session["role"] = user[1]

            flash("Login successful!")

            if user[1] == "admin":
                return redirect("/admin")
            elif user[1] == "executive":
                return redirect("/executive")
            else:
                return redirect("/user")

        else:
            flash("Invalid email or password")
            return redirect("/")

    return render_template("login.html")



@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        import re

        # ✅ PHONE VALIDATION
        pattern = r"^[6-9]\d{9}$"

        if not re.match(pattern, phone):
            flash("Invalid phone number! Must be 10 digits and start with 6-9")
            return redirect("/register")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        existing = cur.fetchone()

        if existing:
            flash("Email already registered!")
            conn.close()
            return redirect("/register")

        cur.execute("""INSERT INTO users (name, email, phone, password, role, status)
            VALUES (?, ?, ?, ?, 'user', 'Waiting')""",
            (name, email, phone, password))

        conn.commit()
        conn.close()

        flash("Registration submitted! Wait for approval.")
        return redirect("/")

    return render_template("register.html")



@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")