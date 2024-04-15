import sqlite3

conn = sqlite3.connect('./../news.db')

cursor = conn.execute("SELECT id from TasnimNews")
for row in cursor:
    conn.execute(f"DELETE from TasnimNews where id = {row[0]};")


conn.commit()
conn.close()
