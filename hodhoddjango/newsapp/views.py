from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from .models import News, Topic, NewsAgency
import pandas as pd
import numpy as np
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

from main import record, rating, deleteRating, readRating


def news(request):

    # if request.user.is_authenticated:
    #     username = request.user.username
    # else:
    #     username = "sampleUser"
    
    return render(request, "index.html")

def stream_articles(request, count = 0):
    start = time.time()
    print('----------started----------')


    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "sampleUser"
    
    try:
        with open(f'../pickles/{username}_MLP.pkl', 'rb') as f:
            mlp = pickle.load(f)
        with open(f'../pickles/{username}_tfidfTitle.pkl', 'rb') as f:
            tfidf_title = pickle.load(f)
        with open(f'../pickles/{username}_tfidfAbs.pkl', 'rb') as f:
            tfidf_abstract = pickle.load(f)
        with open(f'../pickles/{username}_agency.pkl', 'rb') as f:
            trained_news_agency_columns = pickle.load(f)
        flag = False
    except:
        flag = True
        mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns = 0, 0, 0, 0
            
    print('loading pickles:',time.time()-start)

    oldnews = News.objects.filter(published__gte=int(time.time())-432000)
    # oldnews = News.objects.all()

    news = {0: [],1: [],2: [],3: [],4: [],5: []}
    ids = []
    rating = readRating(username)
    for e in rating:
        try:
            x = list(filter(lambda x: x.id == e[0], oldnews))[0]
        except:
            continue
        ids.append(e[0])

        i = int(e[1])
        if i in [0,1,2,3,4,5]:
            news[i].append(x)
        elif i > 5:
            news[5].append(x)
        else:
            news[0].append(x)
    
    newNews = list(filter(lambda x: not x.id in ids, oldnews))
    for e in newNews:
        if flag:
            i = 0
        else:        
            new_data = {"title": e.title, "abstract": e.abstract, "newsAgency": e.newsAgency.title}
            i = int(predict_star(new_data, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns))

        if i in [0,1,2,3,4,5]:
            news[i].insert(0, e)
        elif i > 5:
            news[5].insert(0, e)
        else:
            news[0].insert(0, e)

    lnews = news[5] + news[4] + news[3] + news[2] + news[1] + news[0]
    lnews = list(dict.fromkeys(lnews))
    x = []
    c = int(count)
    try:
        x = lnews[int(c*12):int((c+1)*12)]
    except:
        x = lnews[int(c*12):]
        

    print("newNews:", len(newNews))
    print('loading news:',time.time()-start)
    def regressor(x, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns, username, count):
        # now = time.time()
        for thenews in x:
            n = {}
            n["id"] = thenews.id
            n["newsAgency"] = thenews.newsAgency.title
            n["title"] = thenews.title
            # n["abstract"] = thenews.abstract[:150] + "..."
            n["abstract"] = thenews.abstract
            date = int(thenews.published)
            date = datetime.datetime.fromtimestamp(date)
            date = pytz.timezone("GMT").localize(date)
            date = date.astimezone(pytz.timezone("Asia/Tehran"))
            jdate = jdatetime.datetime.fromgregorian(year=date.year,month=date.month,day=date.day, hour=date.hour, minute=date.minute, second=date.second)
            # if (int(now) - int(thenews.published)) > 432000:
            #     continue
            n["published"] = str(jdate)
            n["published"] = "".join(list(map(lambda x: x in "1234567890" and "۰۱۲۳۴۵۶۷۸۹"[int(x)] or x, n["published"])))
            topic = thenews.topic.title
            n["topic"] = topic
            n["image"] = thenews.image
            n["link"] = thenews.link
            if flag:
                n['stars'] = 0
            else:
                new_data = {"title": n["title"], "abstract": n["abstract"], "newsAgency": n["newsAgency"]}
                n['stars'] = str(predict_star(new_data, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns))
            if len(n['abstract']) > 150:
                n['abstract'] = n['abstract'][:150] + '...'

            yield f"data: {json.dumps(n)}\n\n"

        print('end regressing:',time.time()-start)
        if int(count) == 0 and flag == False:
            saveAllNewsRating(username, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns)
        print('end saving:',time.time()-start)

    response = StreamingHttpResponse(regressor(x, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns, username, count), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
    

def saveAllNewsRating(username, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns):
    deleteRating(username)
    news = News.objects.all()
    for i in news:
        new_data = {"title": i.title, "abstract": i.abstract, "newsAgency": i.newsAgency.title}
        star = int(predict_star(new_data, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns))
        rating(username, i.id, star)

def newsRating(request):
    result = dict(request.GET)
    n = float(result["result[n]"][0])
    id = result["result[id]"][0]
    if request.user.is_authenticated:
        username = request.user.username
    else:
        return JsonResponse({"404":"User Not Found"})
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
        news = News(id=row[0], title=row[1], abstract=row[3], link=row[5], published=int(float(row[6])), image=row[7], newsAgency=newsAgency)
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

def predict_star(new_data, mlp, tfidf_title, tfidf_abstract, trained_news_agency_columns):
    X_title_new = tfidf_title.transform([new_data['title']])
    X_abstract_new = tfidf_abstract.transform([new_data['abstract']])
    news_agency_dummies_new = pd.get_dummies(new_data['newsAgency'])
    for col in trained_news_agency_columns:
        if col not in news_agency_dummies_new:
            news_agency_dummies_new[col] = 0
    news_agency_dummies_new = news_agency_dummies_new[trained_news_agency_columns]
    X_new = np.hstack((X_title_new.toarray(), X_abstract_new.toarray(), news_agency_dummies_new.values))
    predicted_ratings = mlp.predict(X_new)

    return predicted_ratings[0]


