from bs4 import BeautifulSoup
import feedparser
import requests
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
        if (id in ids):
            print("Exist")
            continue

        pub = entry.published_parsed
        pub = time.mktime(pub)

        soup = BeautifulSoup(requests.get(entry.link).content, "html.parser")
        p = soup.find("p", class_="lead p-2 text-justify radius").text
        abstract = p.strip()

        cursor.execute(f"INSERT INTO FarsNews VALUES ('{id}', '{entry.title}', '{abstract}', '{entry.link}', '{pub}')")
        print("Added")
        

    print("commited")

    conn.commit() 
  
    conn.close()


crawler()


"""CREATE TABLE FarsNews
(id TEXT PRIMARY KEY NOT NULL,
title TEXT NOT NULL,
abstract TEXT NOT NULL,
link TEXT NOT NULL,
published TEXT NOT NULL);"""