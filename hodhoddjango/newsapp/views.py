from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from .models import News, Topic, NewsAgency
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

from main import record, rating

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


def news(request):

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/accounts/signup/")
    
    return render(request, "index.html")

def stream_articles(request, count = 0):
    start = time.time()
    print('----------started----------')

    username = "mahdi"

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


    oldnews = News.objects.all()

    c = int(count)
    try:
        x = oldnews[int(c*12):int((c+1)*12)]
    except:
        x = oldnews[int(c*12):]
        

    print('loading news:',time.time()-start)
    def regressor(x, model, vectorizer):
        # now = time.time()
        for thenews in x:
            n = {}
            n["id"] = thenews.id
            n["title"] = thenews.title
            # n["abstract"] = thenews.abstract[:150] + "..."
            n["abstract"] = thenews.abstract
            date = int(thenews.published[:-2])
            date = datetime.datetime.fromtimestamp(date)
            date = pytz.timezone("GMT").localize(date)
            date = date.astimezone(pytz.timezone("Asia/Tehran"))
            jdate = jdatetime.datetime.fromgregorian(year=date.year,month=date.month,day=date.day, hour=date.hour, minute=date.minute, second=date.second)
            # if (int(now) - int(thenews.published[:-2])) > 345600:
            #     print(int(now) - int(thenews.published[:-2]), jdate)
            #     continue
            n["published"] = str(jdate)
            topic = thenews.topic.title
            n["topic"] = topic
            n["image"] = thenews.image
            n["link"] = thenews.link
        
            n['stars'] = str(predict_star(n['title'] + "\n" + n['abstract'], model, vectorizer))
            if len(n['abstract']) > 150:
                n['abstract'] = n['abstract'][:150] + '...'

            yield f"data: {json.dumps(n)}\n\n"

        print('end regressing:',time.time()-start)

        
    response = StreamingHttpResponse(regressor(x, model, vectorizer), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
    

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

def predict_star(text, model, vectorizer):
    text = str(text)
    text_vectorized = vectorizer.transform([text])
    predicted_star = model.predict(text_vectorized)
    return predicted_star[0]


