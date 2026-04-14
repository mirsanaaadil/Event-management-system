import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("DELETE FROM registrations")

conn.commit()
conn.close()