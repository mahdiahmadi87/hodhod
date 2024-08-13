import feedparser
import requests 
import sqlite3
import time
import sys
import os
import re

module_path = os.path.abspath("../classification/")
sys.path.append(module_path)

from main import classifier

def crawler():
    feed = feedparser.parse("https://www.zoomit.ir/feed/")
    # feed = feedparser.parse("./download.rss")

    conn = sqlite3.connect('./../news.db')

    siteIds = list(conn.execute("SELECT siteId from Zoomit"))
    siteIds = list(map(lambda x: x[0], siteIds))
    ids = list(conn.execute("SELECT id from Zoomit"))
    ids = list(map(lambda x: x[0], ids))
    ids = list(map(int, ids))

    cursor = conn.cursor() 
    i = 1
    for entry in feed.entries:          
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
        topic = classifier(abstract)
        if topic == "استان‌ها":
            topic = "ایران"
        print(topic)

        
        image = entry.summary
        image = re.findall(r'src="https://.*q=\d+"', image)[0][5:-1]
        print(image)

        cursor.execute(f"INSERT INTO Zoomit VALUES ('{id}', '{siteId}', '{entry.title}', '{abstract}', '{topic}',  '{entry.link}', '{pub}', '{image}')")
        conn.commit() 
        print("Added")

    
    print("commited")
    conn.close()
    if i > 1:
        print(requests.get("http://51.68.137.82:11111/dbToDjango/"))


if __name__ == "__main__":
    while True:
        print(u"\033[92mZoomit Crawler Is Running!\033[0m")
        crawler()
        print(u"\033[95mEnd Crawling!\033[0m")
        time.sleep(1)



"""CREATE TABLE Zoomit
(id TEXT PRIMARY KEY NOT NULL,
siteId TEXT NOT NULL,
title TEXT NOT NULL,
abstract TEXT NOT NULL,
topic TEXT NOT NULL,
link TEXT NOT NULL,
published TEXT NOT NULL,
image TEXT NOT NULL);"""


{
    'title': 'پژوهشی تازه: گربه\u200cها ممکن است سوگوار عزیزان ازدست\u200cرفته\u200cشان شوند',
    'title_detail': {
        'type': 'text/plain', 
        'language': None, 
        'base': 'https://www.zoomit.ir/feed/', 
        'value': 'پژوهشی تازه: گربه\u200cها ممکن است سوگوار عزیزان ازدست\u200cرفته\u200cشان شوند'
    }, 
    'published': 'Mon, 12 Aug 2024 18:10:00 GMT', 
    # 'published_parsed': time.struct_time(tm_year=2024, tm_mon=8, tm_mday=12, tm_hour=18, tm_min=10, tm_sec=0, tm_wday=0, tm_yday=225, tm_isdst=0), 
    'links': [
        {
            'rel': 'alternate', 
            'type': 'text/html', 
            'href': 'https://www.zoomit.ir/fundamental-science/425195-cats-might-experience-grief/'
        }
    ], 
    'link': 'https://www.zoomit.ir/fundamental-science/425195-cats-might-experience-grief/', 
    'id': 'https://www.zoomit.ir/fundamental-science/425195-cats-might-experience-grief/', 
    'guidislink': False, 
    'summary': '<a href="https://www.zoomit.ir/fundamental-science/425195-cats-might-experience-grief" target="_blank"><img height="560" src="https://api2.zoomit.ir/media/66b9f39fee7afa9489b3a95e?w=800&amp;q=95" style="padding: 15px 0;" title="پژوهشی تازه: گربه\u200cها ممکن است سوگوار عزیزان ازدست\u200cرفته\u200cشان شوند" width="800" /></a><br /><p>مطالعه\u200cای نشان می\u200cدهد که گربه\u200cها نیز ممکن است پس از مرگ حیوان خانگی دیگر خانه، دچار غم و اندوه شوند و رفتارهایی را در پیش گیرند که نشانه سوگواری است.</p><br />', 
    'summary_detail': {
        'type': 'text/html', 
        'language': None, 
        'base': 'https://www.zoomit.ir/feed/', 
        'value': '<a href="https://www.zoomit.ir/fundamental-science/425195-cats-might-experience-grief" target="_blank"><img height="560" src="https://api2.zoomit.ir/media/66b9f39fee7afa9489b3a95e?w=800&amp;q=95" style="padding: 15px 0;" title="پژوهشی تازه: گربه\u200cها ممکن است سوگوار عزیزان ازدست\u200cرفته\u200cشان شوند" width="800" /></a><br /><p>مطالعه\u200cای نشان می\u200cدهد که گربه\u200cها نیز ممکن است پس از مرگ حیوان خانگی دیگر خانه، دچار غم و اندوه شوند و رفتارهایی را در پیش گیرند که نشانه سوگواری است.</p><br />'
    }, 
    'tags': [
        {
            'term': 'علمی', 
            'scheme': None, 
            'label': None
        }, 
        {
            'term': 'علوم پایه و مهندسی', 
            'scheme': None, 
            'label': None
        }
    ]
}