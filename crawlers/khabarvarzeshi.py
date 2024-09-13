import feedparser
import requests 
import sqlite3
import signal
import time
import sys
import os
import re

module_path = os.path.abspath("../classification/")
sys.path.append(module_path)

from main import classifier

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()


def crawler():
    feed = feedparser.parse("https://www.khabarvarzeshi.com/rss")
    # feed = feedparser.parse("./download.rss")

    conn = sqlite3.connect('./../news.db')

    siteIds = list(conn.execute("SELECT siteId from News"))
    siteIds = list(map(lambda x: x[0], siteIds))
    ids = list(conn.execute("SELECT id from News"))
    ids = list(map(lambda x: x[0], ids))
    ids = list(filter(lambda x: x[:2] == "20", ids))
    ids = list(map(int, ids))

    cursor = conn.cursor() 
    i = 1
    for entry in feed.entries:    
        try:      
            siteId = entry.id
            x = re.findall(r"\/\d{6,}", siteId)
            siteId = x[0][1:]
            if (siteId in siteIds):
                print("Exist")
                continue

            try:
                id = max(ids) + i
                i += 1
            except:
                print("ID Not found! generated to 20100001")
                id = "20100001"
                ids = [20100001]


            pub = entry.published_parsed
            pub = time.mktime(pub)

            abstract = entry.summary
            print("\n" + abstract + ":")
            topic = classifier(str(entry.title) + "\n" + abstract)
            if topic == "استان‌ها":
                topic = "ایران"
            print(topic)

            
            image = entry.links[1].href

            cursor.execute(f"INSERT INTO News VALUES ('{id}', '{siteId}', 'KhabarVarzeshi', '{entry.title}', '{abstract}', '{topic}',  '{entry.link}', '{pub}', '{image}')")
            conn.commit() 
            print("Added")
        except:
            i -= 1
            continue
            

    
    print("commited")
    conn.close()
    try:
        if i > 1:
            print(requests.get("http://51.68.137.82:11111/dbToDjango/"))
    except:
        return


if __name__ == "__main__":
    while True:
        print(u"\033[34mKhabarVarzeshi Crawler Is Running!\033[0m")
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)
            
            crawler()
            
            signal.alarm(0)

        except TimeoutException:
            print("\033[31mExecution time took too long!\033[0m")
            continue

        except Exception as e:
            print(f"\033[31mAn error occurred!\033[0m")
            continue
        print(u"\033[35mEnd Crawling!\033[0m")
        time.sleep(1)