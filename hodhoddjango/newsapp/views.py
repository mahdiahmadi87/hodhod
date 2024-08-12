from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import News, Topic, NewsAgency
from hazm import Normalizer 
import pandas as pd
import jdatetime
import sqlite3
import pickle
import time
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
    # fromDbToDjango("FarsNews")
    fromDbToDjango("TasnimNews")
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
        date = time.localtime(int(thenews.published[:-2]))
        date = jdatetime.date.fromgregorian(year=date.tm_year,month=date.tm_mon,day=date.tm_mday)
        n["published"] = f"{date.year}/{date.month}/{date.day}"
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

def fromDbToDjango(newsAgency):
    newsAgency = NewsAgency.objects.filter(title=newsAgency)[0]

    conn = sqlite3.connect('./../news.db')

    cursor = list(conn.execute(f"SELECT id, title, abstract, topic, link, published, image from {newsAgency.title}"))

    for row in cursor:
        news = News(id=row[0], title=row[1], abstract=row[2], link=row[4], published=row[5], image=row[6], newsAgency=newsAgency)
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


    # مرتب‌سازی DataFrame بر اساس ستون score
    sorted_results = results.sort_values(by='stars', ascending=False)

    sorted_news = sorted_results.to_dict(orient='records')
    return sorted_news

