from flask import Blueprint, redirect, request, render_template, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

admin = Blueprint("admin", __name__)


 
@admin.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # events
    cur.execute("SELECT * FROM events ORDER BY date ASC")
    events = cur.fetchall()

    # executives
    cur.execute("SELECT * FROM users WHERE role='executive'")
    executives = cur.fetchall()

    # pending users
    cur.execute("SELECT * FROM users WHERE role='user' AND status='Waiting'")
    pending_users = cur.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        events=events,
        users=executives,          # ✅ executives
        pending_users=pending_users
    )



@admin.route("/add_event", methods=["POST"])
def add_event():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    name = request.form["name"]
    date = request.form["date"]
    description = request.form["description"]

    UPLOAD_FOLDER = "static/uploads"
    photo = request.files["photo"]
    if photo and photo.filename != "":
        filename = secure_filename(photo.filename)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        photo.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        filename = "default.png"

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO events (name, date, photo, description)
        VALUES (?, ?, ?, ?)
    """, (name, date, filename, description))

    conn.commit()
    conn.close()

    flash("Event added successfully!")
    return redirect("/admin")


@admin.route("/delete_event/<int:id>")
def delete_event(id):
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM events WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("Event deleted successfully!")
    return redirect("/admin")



@admin.route("/add_executive", methods=["POST"])
def add_executive():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # check duplicate username
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if cur.fetchone():
        flash("Username already exists!")
        conn.close()
        return redirect("/admin")

   
    cur.execute("""INSERT INTO users (name, email, phone, username, password, role, status)
    VALUES (?, ?, ?, ?, ?, 'executive', 'approved')""", (name, email, phone, username, password))

    conn.commit()
    conn.close()

    flash("Executive Officer added successfully!")
    return redirect("/admin")


@admin.route("/delete_user/<int:id>")
def delete_user(id):
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("User deleted successfully!")
    return redirect("/admin")

@admin.route("/approve_user/<int:id>")
def approve_user(id):
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE users SET status='Approved' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("User approved successfully!")
    return redirect("/admin")

@admin.route("/reject_user/<int:id>")
def reject_user(id):
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("User rejected!")
    return redirect("/admin")


@admin.route("/registrations")
def view_registrations():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT users.username, events.name, events.date, registrations.status
        FROM registrations
        JOIN users ON registrations.user_id = users.id
        JOIN events ON registrations.event_id = events.id
        ORDER BY events.date
    """)

    registrations = cur.fetchall()
    conn.close()

    return render_template("view_registrations.html", registrations=registrations)


@admin.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")