import sqlite3

conn = sqlite3.connect('./../userNews.db')

usernames = list(set(conn.execute("SELECT username from Users")))

for row in usernames:
    conn.execute(f"DELETE from Users where username = '{row[0]}';")


conn.commit()
conn.close()
