import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# ❗ delete all users
cur.execute("DELETE FROM users")

# ❗ insert admin only
cur.execute("""
    INSERT INTO users (name, email, phone, password, role, status)
    VALUES (?, ?, ?, ?, ?, ?)
""", ("Admin", "admin@gmail.com", "9999999999", "admin123", "admin", "Approved"))

conn.commit()
conn.close()