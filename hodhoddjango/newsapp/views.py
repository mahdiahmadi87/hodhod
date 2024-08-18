from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import News, Topic, NewsAgency
from hazm import Normalizer 
import pandas as pd
import jdatetime
import datetime
import sqlite3
import pickle
import time
import pytz
import json
import sys
import os

module_path = os.path.abspath("../newsSelection/")
sys.path.append(module_path)

from main import selection, record

class SimpleModel:
    def __init__(self):
        pass

    def predict(self, input_text):
        return [0]
    
class SimpleVectorizer:
    def __init__(self):
        pass

    def transform(self, input):
        return input

def select(request):
    topics = Topic.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/accounts/login/")
    if request.GET:
        data = dict(request.GET)["topic"]
        l = []
        for d in data:
            d = int(d)
            topics = list(topics)
            d = list(filter(lambda x: x.id == d, topics))[0]
            l.append(d)
        l = list(map(lambda x: x.title, l))

        selection(username, l)
        return redirect("/")

    return render(request, "select.html", context={"topics": topics})


def news(request):
    oldnews = News.objects.all()
    suggested = []

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/accounts/login/")

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
        # date = time.gmtime(int(thenews.published[:-2]))
        # print(date)
        # date =  datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min, date.tm_sec, 0).astimezone(pytz.timezone("Asia/Tehran"))
        # print(date)
        # print("-----")
        # # jdate = jdatetime.datetime.fromgregorian(year=date.tm_year,month=date.tm_mon,day=date.tm_mday, hour=date.tm_hour, minute=date.tm_min, second=date.tm_sec)
        # jdate = jdatetime.datetime.fromgregorian(year=date.year,month=date.month,day=date.day, hour=date.hour, minute=date.minute, second=date.second)
        # n["published"] = f"{jdate.year}/{jdate.month}/{jdate.day} {jdate.hour}:{jdate.minute}"
        date = int(thenews.published[:-2])
        date = datetime.datetime.fromtimestamp(date)
        print(date)
        date = pytz.timezone("GMT").localize(date)
        print(date)
        date = date.astimezone(pytz.timezone("Asia/Tehran"))
        jdate = jdatetime.datetime.fromgregorian(year=date.year,month=date.month,day=date.day, hour=date.hour, minute=date.minute, second=date.second)
        print(date)
        n["published"] = str(jdate)
        topic = thenews.topic.title
        n["topic"] = topic
        n["image"] = thenews.image
        n["link"] = thenews.link
        if topic in interests:
            suggested.append(n)
    
    sorted_news = regressor(suggested, username)
    jsonNews = json.dumps(suggested)
    return render(request, "index.html", context={"suggested": sorted_news, "jsoned": jsonNews})

def newsRating(request):
    result = dict(request.GET)
    n = float(result["result[n]"][0])
    id = result["result[id]"][0]
    username = request.user.username
    record(username, id, n)
    return JsonResponse({})

def dbToDjango(requests):
    fromDbToDjango()
    return HttpResponse("OK")

def fromDbToDjango():

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute(f"SELECT id, title, newsAgency, abstract, topic, link, published, image from News"))

    for row in cursor:
        try:
            newsAgency = NewsAgency.objects.filter(title=row[2])[0]
        except:
            newsAgency = NewsAgency(title=row[2])
            newsAgency.save()
        for i in range(len(row)):
            print(i, ":", row[i])
        news = News(id=row[0], title=row[1], abstract=row[3], link=row[5], published=row[6], image=row[7], newsAgency=newsAgency)
        old = News.objects.all()
        if news in old:
            continue
        news.save()

        topic = row[4]
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
        news.topic = newtopics

        news.save()

def predict_star(text, model, vectorizer, normalizer):
    text = str(text)
    text_normalized = normalizer.normalize(text)
    text_vectorized = vectorizer.transform([text_normalized])
    predicted_star = model.predict(text_vectorized)
    return predicted_star[0]

def regressor(news, username):
    try:
        filename = f"../pickles/{username}_regressor.pkl"
        with open(filename, 'rb') as f:
            model = pickle.load(f)
            
        filename = f"../pickles/{username}_vectorizer.pkl"
        with open(filename, 'rb') as f:
            vectorizer = pickle.load(f)
    except:
        model = SimpleModel()
        vectorizer = SimpleVectorizer()

    normalizer = Normalizer()


    # پیش‌بینی خروجی برای هر دیکشنری و ذخیره آنها در یک DataFrame
    results = pd.DataFrame(news)
    results['stars'] = results['abstract'].apply(lambda x: predict_star(x, model, vectorizer, normalizer))
    results['sort'] = results['stars'].apply(lambda x: str(x)[:3]) + results["published"].apply(lambda x: x[5:])

    # مرتب‌سازی DataFrame بر اساس ستون score
    sorted_results = results.sort_values(by='sort', ascending=False)

    sorted_news = sorted_results.to_dict(orient='records')
    return sorted_news

