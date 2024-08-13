import feedparser
import requests
import sqlite3
import time
import sys
import os

module_path = os.path.abspath("../classification/")
sys.path.append(module_path)

from main import classifier

def crawler():
    feed = feedparser.parse("https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%AE%D8%A8%D8%B1%D9%87%D8%A7%DB%8C-%D8%B1%D9%88%D8%B2")

    conn = sqlite3.connect('./../news.db')

    siteIds = list(conn.execute("SELECT siteId from News"))
    siteIds = list(map(lambda x: x[0], siteIds))
    ids = list(conn.execute("SELECT id from News"))
    ids = list(map(lambda x: x[0], ids))
    ids = list(filter(lambda x: x[:2] == "10", ids))
    ids = list(map(int, ids))

    cursor = conn.cursor() 
    i = 1
    for entry in feed.entries:  
        siteId = entry.id
        siteId = siteId[-7:]
        if (siteId in siteIds):
            print("Exist")
            continue

        try:
            id = max(ids) + i
            i += 1
        except:
            print("ID Not found! generated to 10100001")
            id = "10100001"
            ids = [10100001]


        pub = entry.published_parsed
        pub = time.mktime(pub)

        abstract = entry.summary
        print("\n" + abstract + ":")
        topic = classifier(abstract)
        if topic == "استان‌ها":
            topic = "ایران"
        print(topic)

        
        image = entry.media_thumbnail[0]["url"]

        cursor.execute(f"INSERT INTO News VALUES ('{id}', '{siteId}', 'TasnimNews', '{entry.title}', '{abstract}', '{topic}',  '{entry.link}', '{pub}', '{image}')")
        conn.commit() 
        print("Added")
        
        
    print("commited")
    conn.close()
    try:
        if i > 1:
            print(requests.get("http://51.68.137.82:11111/dbToDjango/"))
    except:
        return


if __name__ == "__main__":
    while True:
        print(u"\033[92mTasnim Crawler Is Running!\033[0m")
        crawler()
        print(u"\033[95mEnd Crawling!\033[0m")
        time.sleep(1)


