from django.contrib import admin
from .models import News, Topic, NewsAgency

# Register your models here.

admin.site.register(News)
admin.site.register(Topic)
admin.site.register(NewsAgency)
