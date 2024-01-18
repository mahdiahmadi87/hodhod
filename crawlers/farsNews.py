import feedparser
import sqlite3

def crawler():
    feed = feedparser.parse("https://www.farsnews.ir/rss")
    # feed = feedparser.parse("./rss")
    
    news = []

    for entry in feed.entries:
        theNews = {}
        theNews['id'] = entry.id
        theNews['id'] = theNews['id'][-14:]
        theNews['title'] = entry.title
        theNews['link'] = entry.link
        news.append(theNews)

    return news


def insert():
    news = crawler()
    conn = sqlite3.connect('./../news.db')
        

    cursor = list(conn.execute("SELECT id from FarsNews"))
    ids = list(map(lambda x: str(x[0]), cursor))

    cursor = conn.cursor() 

    for theNews in news:
        if (theNews["id"] in ids):
            print("Exist")
        else:
            cursor.execute(f"INSERT INTO FarsNews VALUES ({theNews['id']}, '{theNews['title']}', '{theNews['link']}')")
            print("Added")

    print("commited")

    conn.commit() 
  
    conn.close()


insert()

"""CREATE TABLE FarsNews
(id INT PRIMARY KEY NOT NULL,
title TEXT NOT NULL,
link TEXT NOT NULL);"""