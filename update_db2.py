import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("ALTER TABLE events ADD COLUMN photo TEXT")

conn.commit()
conn.close()