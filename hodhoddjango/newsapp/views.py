from django.http import HttpResponse
from django.shortcuts import render
from .models import News, Tag, Topic, NewsAgency
import jdatetime
import sqlite3
import time

# Create your views here.
def index(request):
    news = []
    oldnews = News.objects.all()[:8]
    for thenews in oldnews:
        n = {}
        n["id"] = thenews.id
        n["title"] = thenews.title
        n["abstract"] = thenews.abstract[:150] + "..."
        date = time.localtime(int(thenews.published[:-2]))
        date = jdatetime.date.fromgregorian(year=date.tm_year,month=date.tm_mon,day=date.tm_mday)
        n["published"] = f"{date.year}/{date.month}/{date.day}"
        news.append(n)
        tags = thenews.tags.all().values()
        tags = list(map(lambda x: x['title'], tags))
        n["tags"] = tags
    return render(request, "index.html", context={"news": news})

def news(request):
    fromDbToDjango("FarsNews")
    oldnews = News.objects.all()
    news = []
    for thenews in oldnews:
        n = {}
        n["id"] = thenews.id
        n["title"] = thenews.title
        n["abstract"] = thenews.abstract[:150] + "..."
        date = time.localtime(int(thenews.published[:-2]))
        date = jdatetime.date.fromgregorian(year=date.tm_year,month=date.tm_mon,day=date.tm_mday)
        n["published"] = f"{date.year}/{date.month}/{date.day}"
        news.append(n)
        tags = thenews.tags.all().values()
        tags = list(map(lambda x: x['title'], tags))
        n["tags"] = tags
    return render(request, "news.html", context={"news": news})


def fromDbToDjango(newsAgency):
    newsAgency = NewsAgency.objects.filter(title="FarsNews")[0]

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute(f"SELECT id, title, abstract, tags, topics, link, published from {newsAgency.title}"))

    for row in cursor:
        news = News(id=row[0], title=row[1], abstract=row[2], link=row[5], published=row[6], newsAgency=newsAgency)
        old = News.objects.all()
        if news in old:
            continue
        news.save()
        tags = row[3].split("|")
        oldtags = Tag.objects.all()
        newtags = []
        for tag in tags:
            exist = list(filter(lambda x: x.title == tag, oldtags))
            if (len(exist) > 0):
                exist = exist[0]
                newtags.append(exist)
            else:
                tag = Tag(title=tag)
                tag.save()
                newtags.append(tag)
        news.tags.set(newtags)

        topics = row[4].split("|")
        oldtopics = Topic.objects.all()
        newtopics = []
        if (topics == ['']):
            topics = []
        for topic in topics:
            exist = list(filter(lambda x: x.title == topic, oldtopics))
            if (len(exist) > 0):
                exist = exist[0]
                newtopics.append(exist)
            else:
                topic = Topic(title=topic)
                topic.save()
                newtopics.append(topic)
        news.topics.set(newtopics)

        news.save()
