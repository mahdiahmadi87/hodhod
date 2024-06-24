from .models import News, Topic, NewsAgency
from django.contrib import admin

# Register your models here.

admin.site.register(NewsAgency)
admin.site.register(Topic)
admin.site.register(News)
