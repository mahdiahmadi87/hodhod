import sqlite3

conn = sqlite3.connect('./../news.db')


conn.execute(f"DELETE from News")


conn.commit()
conn.close()

"""CREATE TABLE News
(id TEXT PRIMARY KEY NOT NULL,
siteId TEXT NOT NULL,
newsAgency TEXT NOT NULL,
title TEXT NOT NULL,
abstract TEXT NOT NULL,
topic TEXT NOT NULL,
link TEXT NOT NULL,
published TEXT NOT NULL,
image TEXT NOT NULL);"""