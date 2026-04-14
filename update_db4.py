import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# add new columns
cur.execute("ALTER TABLE users ADD COLUMN name TEXT")
cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
cur.execute("ALTER TABLE users ADD COLUMN phone TEXT")
cur.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'Waiting'")
cur.execute("""
    DELETE FROM users 
    WHERE username IN ('user1', 'user2', 'user3', 'asif')
""")

conn.commit()
conn.close()