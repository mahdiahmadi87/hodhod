import feedparser
import sqlite3
import time

import sys
import os


module_path = os.path.abspath("../classification/")
sys.path.append(module_path)

from main import q

def crawler():
    feed = feedparser.parse("https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%AE%D8%A8%D8%B1%D9%87%D8%A7%DB%8C-%D8%B1%D9%88%D8%B2")
    # feed = feedparser.parse("./rss")
    print(feed)

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute("SELECT id from TasnimNews"))
    ids = list(map(lambda x: x[0], cursor))

    cursor = conn.cursor() 

    for entry in feed.entries:  
        id = entry.id
        id = id[-7:]
        if (id in ids):
            print("Exist")
            continue

        pub = entry.published_parsed
        pub = time.mktime(pub)

        abstract = entry.summary
        print("\n" + abstract, ":")
        topic = classifier(abstract)
        print(topic)

        cursor.execute(f"INSERT INTO TasnimNews VALUES ('{id}', '{entry.title}', '{abstract}', '{topic}',  '{entry.summary_detail.base}', '{pub}')")
        conn.commit() 
        print("Added")
        
        

    print("commited")

  
    conn.close()

crawler()


"""CREATE TABLE TasnimNews
(id TEXT PRIMARY KEY NOT NULL,
title TEXT NOT NULL,
abstract TEXT NOT NULL,
topics TEXT NOT NULL,
link TEXT NOT NULL,
published TEXT NOT NULL);"""