from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import News, Topic, NewsAgency
import jdatetime
import sqlite3
import time
import os
import sys

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
        topic = thenews.topic
        n["topic"] = topic
        news.append(n)
    return render(request, "index.html", context={"news": news})

def select(request):
    topics = Topic.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/accounts/google/login/")
    if request.GET:
        data = dict(request.GET)["topic"]
        l = []
        for d in data:
            d = int(d)
            topics = list(topics)
            d = list(filter(lambda x: x.id == d, topics))[0]
            l.append(d)
        l = list(map(lambda x: x.title, l))
        print(l)

        module_path = os.path.abspath("../newsSelection/")
        sys.path.append(module_path)

        from main import selection

        selection(username, l)
        return redirect("/")

    return render(request, "select.html", context={"topics": topics})


def thenews(request, slug):
    thenews = News.objects.get(id=slug)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/accounts/google/login/")

    n = {}
    n["id"] = thenews.id
    n["title"] = thenews.title
    n["abstract"] = thenews.abstract
    date = time.localtime(int(thenews.published[:-2]))
    date = jdatetime.date.fromgregorian(year=date.tm_year,month=date.tm_mon,day=date.tm_mday)
    n["published"] = f"{date.year}/{date.month}/{date.day}"
    topic = thenews.topic.title
    n["topic"] = topic 
    return render(request, "thenews.html", context={"news": n})

def news(request):
    # fromDbToDjango("FarsNews")
    fromDbToDjango("TasnimNews")
    oldnews = News.objects.all()
    news = []
    suggested = []

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/accounts/google/login/")

    conn = sqlite3.connect('./../userNews.db')
    interests = list(conn.execute(f"SELECT interest from Interests where username = '{username}'"))
    interests = list(map(lambda x: x[0], interests))
    interests = list(set(interests))
    conn.close()
    
    for thenews in oldnews:
        n = {}
        n["id"] = thenews.id
        n["title"] = thenews.title
        # n["abstract"] = thenews.abstract[:150] + "..."
        n["abstract"] = thenews.abstract
        date = time.localtime(int(thenews.published[:-2]))
        date = jdatetime.date.fromgregorian(year=date.tm_year,month=date.tm_mon,day=date.tm_mday)
        n["published"] = f"{date.year}/{date.month}/{date.day}"
        topic = thenews.topic.title
        n["topic"] = topic
        if topic in interests:
            suggested.append(n)
        else:
            news.append(n)

    return render(request, "news.html", context={"news": news, "suggested": suggested})


def fromDbToDjango(newsAgency):
    newsAgency = NewsAgency.objects.filter(title=newsAgency)[0]

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute(f"SELECT id, title, abstract, topic, link, published from {newsAgency.title}"))

    for row in cursor:
        news = News(id=row[0], title=row[1], abstract=row[2], link=row[4], published=row[5], newsAgency=newsAgency)
        old = News.objects.all()
        if news in old:
            continue
        news.save()

        topic = row[3]
        oldtopics = Topic.objects.all()
        newtopics = []
        exist = list(filter(lambda x: x.title == topic, oldtopics))
        if (len(exist) > 0):
            exist = exist[0]
            newtopics = exist
        else:
            topic = Topic(title=topic)
            topic.save()
            newtopics = topic
        print("**********", dir(news.topic))
        news.topic = newtopics

        news.save()
