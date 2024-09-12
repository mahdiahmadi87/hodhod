import feedparser
import requests 
import signal
import sqlite3
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
    feed = feedparser.parse("https://www.zoomit.ir/feed/")
    # feed = feedparser.parse("./download.rss")

    conn = sqlite3.connect('./../news.db')

    siteIds = list(conn.execute("SELECT siteId from News"))
    siteIds = list(map(lambda x: x[0], siteIds))
    ids = list(conn.execute("SELECT id from News"))
    ids = list(map(lambda x: x[0], ids))
    ids = list(filter(lambda x: x[:2] == "15", ids))
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
                print("ID Not found! generated to 15100001")
                id = "15100001"
                ids = [15100001]


            pub = entry.published_parsed
            pub = time.mktime(pub)

            abstract = entry.summary
            abstract = re.findall(r"\<p\>.*\<\/p\>", abstract)[0][3:-4]
            print("\n" + abstract + ":")
            topic = classifier(str(entry.title) + "\n" + abstract)
            if topic == "استان‌ها":
                topic = "ایران"
            print(topic)

            
            image = entry.summary
            image = re.findall(r'src="https://.*q=\d+"', image)[0][5:-1]

            cursor.execute(f"INSERT INTO News VALUES ('{id}', '{siteId}', 'Zoomit', '{entry.title}', '{abstract}', '{topic}',  '{entry.link}', '{pub}', '{image}')")
            conn.commit() 
            print("Added")
        except:
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
        print(u"\033[34mZoomit Crawler Is Running!\033[0m")
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