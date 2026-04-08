from flask import Blueprint, redirect, request, render_template, session
from datetime import datetime
import sqlite3

admin = Blueprint("admin", __name__)


@admin.route("/admin")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    conn.close()

    
    msg = request.args.get("msg")

    return render_template("admin_dashboard.html", events=events, msg=msg)



@admin.route("/add_event", methods=["POST"])
def add_event():
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    name = request.form["name"]
    date = request.form["date"]
    location = request.form["location"]
    description = request.form["description"]

    today = datetime.today().date()
    event_date = datetime.strptime(date, "%Y-%m-%d").date()

    if event_date < today:
        return "Cannot add past date"

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO events (name, date, location, description) VALUES (?, ?, ?, ?)",
                (name, date, location, description))

    conn.commit()
    conn.close()

    return redirect("/admin?msg=added")


@admin.route("/delete_event/<int:id>")
def delete_event(id):
    if "role" not in session or session["role"] != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM events WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")


@admin.route("/registrations")
def view_registrations():
    if session.get("role") != "admin":
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT users.username, events.name
        FROM registrations
        JOIN users ON registrations.user_id = users.id
        JOIN events ON registrations.event_id = events.id
    """)

    registrations = cur.fetchall()
    conn.close()

    return render_template("view_registrations.html", registrations=registrations)

def logout():
    session.clear() 
    flash("Logged out successfully!")
    return redirect("/") 