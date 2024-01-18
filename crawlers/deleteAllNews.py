import sqlite3

conn = sqlite3.connect('./../news.db')

cursor = conn.execute("SELECT id from FarsNews")
for row in cursor:
    conn.execute(f"DELETE from FarsNews where id = {row[0]};")


conn.commit()
conn.close()
