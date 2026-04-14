from flask import Blueprint, render_template, redirect, session, flash
import sqlite3

user = Blueprint("user", __name__)


# ---------------- CHECK USER ----------------
def check_user():
    return session.get("role") == "user"


# ---------------- USER DASHBOARD ----------------
@user.route("/user")
def user_dashboard():
    if not check_user():
        return redirect("/")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # ✅ FIX: handle NULL photo
    cur.execute("""
        SELECT id, name, date,
               COALESCE(photo, 'default.png'),
               description
        FROM events
    """)
    events = cur.fetchall()

    # already registered
    cur.execute("SELECT event_id FROM registrations WHERE user_id=?", (user_id,))
    registered = [r[0] for r in cur.fetchall()]

    conn.close()

    return render_template("user_dashboard.html",
                           events=events,
                           registered=registered)


# ---------------- REGISTER EVENT ----------------
@user.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    if not check_user():
        return redirect("/")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # prevent duplicate
    cur.execute("""
        SELECT * FROM registrations
        WHERE user_id=? AND event_id=?
    """, (user_id, event_id))

    if cur.fetchone():
        flash("Already registered!")
        conn.close()
        return redirect("/user")

    # insert
    cur.execute("""
        INSERT INTO registrations (user_id, event_id, status)
        VALUES (?, ?, 'Waiting')
    """, (user_id, event_id))

    conn.commit()
    conn.close()

    flash("Registered successfully! Waiting for approval.")
    return redirect("/my_events")


# ---------------- MY EVENTS ----------------
@user.route("/my_events")
def my_events():
    if not check_user():
        return redirect("/")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""SELECT events.name, events.date, COALESCE(events.photo, 'default.png'), registrations.status
        FROM registrations
        JOIN events ON events.id = registrations.event_id
        WHERE registrations.user_id=?
    """, (user_id,))

    data = cur.fetchall()
    conn.close()

    return render_template("my_events.html", events=data)



@user.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")