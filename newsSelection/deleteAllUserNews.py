import sqlite3

conn = sqlite3.connect('./../userNews.db')

usernames = list(set(conn.execute("SELECT username from Viewed")))

for row in usernames:
    conn.execute(f"DELETE from Viewed where username = '{row[0]}';")
    conn.execute(f"DELETE from Interests where username = '{row[0]}';")


conn.commit()
conn.close()
