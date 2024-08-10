import sqlite3

conn = sqlite3.connect('./../userNews.db')

usernames = list(set(conn.execute("SELECT username from Viewed")))

for row in usernames:
    conn.execute(f"DELETE from Viewed where username = '{row[0]}';")
    # conn.execute(f"DELETE from Interests where username = '{row[0]}';")


conn.commit()
conn.close()


import sqlite3


tables = ["""CREATE TABLE Viewed
(username TEXT NOT NULL,
newsId TEXT NOT NULL);""",
"""CREATE TABLE Interests
(username TEXT NOT NULL,
interest TEXT NOT NULL);"""]

connection_obj = sqlite3.connect('./userNews.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
for table in tables:
 
    cursor_obj.execute(table)
     
connection_obj.close()
