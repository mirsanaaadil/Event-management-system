import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("UPDATE events SET photo='default.png' WHERE photo IS NULL")

conn.commit()
conn.close()