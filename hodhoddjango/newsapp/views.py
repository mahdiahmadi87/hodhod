from django.http import HttpResponse
from django.shortcuts import render
from .models import News, Tag, Topic, NewsAgency
import sqlite3

# Create your views here.

def homePage(request):
    fromDbToDjango("FarsNews")
    news = News.objects.all().values()
    return render(request, "homePage.html", context={"news": news})


def fromDbToDjango(newsAgency):
    newsAgency = NewsAgency.objects.filter(title="FarsNews")[0]

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute(f"SELECT id, title, abstract, tags, topics, link, published from {newsAgency.title}"))

    for row in cursor:
        news = News(id=row[0], title=row[1], abstract=row[2], link=row[5], published=row[6])
        tags = row[3].split("|")
        oldtags = Tag.objects.all()
        newtags = []
        for tag in tags:
            exist = list(filter(lambda x: x.title == tag, oldtags))
            if (len(exist) > 0):
                exist = exist[0]
                newtags.append(exist)
                # news.tags.add(exist)
            else:
                tag = Tag(title=tag)
                tag.save()
                newtags.append(tag)

        news.tags.set(newtags)
        break
