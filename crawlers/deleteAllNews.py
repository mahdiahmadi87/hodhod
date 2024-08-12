import sqlite3

conn = sqlite3.connect('./../news.db')


conn.execute(f"DELETE from TasnimNews")


conn.commit()
conn.close()
