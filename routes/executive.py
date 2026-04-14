from flask import Blueprint, render_template, redirect, session, flash, request
import sqlite3
import os
from werkzeug.utils import secure_filename

executive = Blueprint("executive", __name__)

UPLOAD_FOLDER = "static/uploads"



def check_executive():
    return session.get("role") == "executive"



def get_db():
    return sqlite3.connect("database.db")



@executive.route("/executive")
def dashboard():
    if not check_executive():
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

   
    cur.execute("""SELECT registrations.id, users.username, events.name, events.date, registrations.status
        FROM registrations
        JOIN users ON users.id = registrations.user_id
        JOIN events ON events.id = registrations.event_id
        ORDER BY events.date""")
    data = cur.fetchall()


    cur.execute("SELECT * FROM users WHERE role='user'")
    users = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE role='user' AND status='Waiting'")
    pending_users = cur.fetchall()

    conn.close()

    return render_template(
        "executive_dashboard.html",
        data=data,
        users=users,
        pending_users=pending_users
    )



@executive.route("/add_event_exec", methods=["POST"])
def add_event():
    if not check_executive():
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

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO events (name, date, photo, description)
        VALUES (?, ?, ?, ?)
    """, (name, date, filename, description))

    conn.commit()
    conn.close()

    flash("Event added successfully!")
    return redirect("/executive")



@executive.route("/approve_user_exec/<int:id>")
def approve_user(id):
    if not check_executive():
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE users SET status='Approved' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("User approved!")
    return redirect("/executive")


@executive.route("/reject_user_exec/<int:id>")
def reject_user(id):
    if not check_executive():
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("User rejected!")
    return redirect("/executive")



@executive.route("/approve/<int:id>")
def approve(id):
    if not check_executive():
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE registrations
        SET status = 'Approved'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    flash("Registration Approved")
    return redirect("/executive")



@executive.route("/reject/<int:id>")
def reject(id):
    if not check_executive():
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE registrations
        SET status = 'Rejected'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    flash("Registration Rejected")
    return redirect("/executive")



@executive.route("/executive_logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")