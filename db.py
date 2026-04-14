import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()


cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, name TEXT, date TEXT, location TEXT, description TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS registrations(id INTEGER PRIMARY KEY, user_id INTEGER, event_id INTEGER)")


cur.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin')")
cur.execute("INSERT OR IGNORE INTO users VALUES (2, 'user1', 'user123', 'user')")
cur.execute("INSERT OR IGNORE INTO users VALUES (3, 'user2', 'user123', 'user')")
cur.execute("INSERT OR IGNORE INTO users VALUES (4, 'user3', 'user123', 'user')")
cur.execute("INSERT OR IGNORE INTO users VALUES (5, 'asif', 'asif123', 'user')")

conn.commit()
conn.close()

print("database created successfully")