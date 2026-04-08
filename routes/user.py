from flask import Blueprint, render_template, redirect, session, flash
import sqlite3

user = Blueprint("user", __name__)

# ---------------- USER DASHBOARD ----------------
@user.route("/user")
def user_dashboard():
    if "role" not in session or session["role"] != "user":
        return redirect("/")

    user_id = int(session.get("user_id"))  # cast to int

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        # Get all events
        cur.execute("SELECT * FROM events")
        events = cur.fetchall()

        # Get registered event IDs
        cur.execute("SELECT event_id FROM registrations WHERE user_id=?", (user_id,))
        registered_ids = [r[0] for r in cur.fetchall()]

    return render_template(
        "user_dashboard.html",
        events=events,
        registered_ids=registered_ids
    )


# ---------------- REGISTER EVENT ----------------
@user.route("/register/<int:event_id>")
def register_event(event_id):
    if "role" not in session or session["role"] != "user":
        return redirect("/")

    user_id = int(session.get("user_id"))

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        # Check if already registered
        cur.execute(
            "SELECT * FROM registrations WHERE user_id=? AND event_id=?",
            (user_id, event_id)
        )
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO registrations (user_id, event_id) VALUES (?, ?)",
                (user_id, event_id)
            )
            conn.commit()  # <-- Important!
            flash("✅ Registered successfully!")
        else:
            flash("⚠️ You already registered for this event!")

    return redirect("/user")


# ---------------- VIEW MY EVENTS ----------------
@user.route("/my_events")
def my_events():
    if "role" not in session or session["role"] != "user":
        return redirect("/")

    user_id = int(session.get("user_id"))

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT events.name, events.date, events.location
            FROM registrations
            JOIN events ON events.id = registrations.event_id
            WHERE registrations.user_id=?
        """, (user_id,))
        events = cur.fetchall()

    return render_template("my_events.html", events=events)

@user.route("/logout")
def logout():
    session.clear()  # removes all session data
    flash("Logged out successfully!")
    return redirect("/")  # go back to login page