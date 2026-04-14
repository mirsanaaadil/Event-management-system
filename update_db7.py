import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
SELECT id, name, photo FROM events;""")

conn.commit()
conn.close()