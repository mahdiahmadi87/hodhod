"""
URL configuration for hodhoddjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("news/", views.news, name="news"),
    path("newsRating/", views.newsRating, name='newsRating'),
    path("select/", views.select, name="select"),
    path("", views.index, name="index"),
    path("news/<slug>", views.thenews,  name="thenews"),
]
