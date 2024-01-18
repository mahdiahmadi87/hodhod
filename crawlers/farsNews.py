import feedparser
import sqlite3
import time

def crawler():
    feed = feedparser.parse("https://www.farsnews.ir/rss")
    # feed = feedparser.parse("./rss")
    

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute("SELECT id from FarsNews"))
    ids = list(map(lambda x: x[0], cursor))

    cursor = conn.cursor() 

    for entry in feed.entries:
        id = entry.id
        id = id[-14:]
        pub = entry.published_parsed
        pub = time.mktime(pub)

        if (id in ids):
            print("Exist")
        else:
            cursor.execute(f"INSERT INTO FarsNews VALUES ('{id}', '{entry.title}', '{entry.link}', '{pub}')")
            print("Added")

    print("commited")

    conn.commit() 
  
    conn.close()


crawler()


"""CREATE TABLE FarsNews
(id TEXT PRIMARY KEY NOT NULL,
title TEXT NOT NULL,
link TEXT NOT NULL,
published TEXT NOT NULL);"""