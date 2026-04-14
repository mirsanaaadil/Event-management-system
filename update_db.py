# db_update.py
import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(registrations)")
columns = [col[1] for col in cur.fetchall()]

if "status" not in columns:
    cur.execute("ALTER TABLE registrations ADD COLUMN status TEXT DEFAULT 'Waiting'")

conn.commit()
conn.close()

print("Database updated ")