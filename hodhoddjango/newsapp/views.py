from django.http import HttpResponse
from django.shortcuts import render
from .models import News

# Create your views here.

def homePage(request):
    news = News.objects.all().values()
    return render(request, "homePage.html", context={"news": news})
