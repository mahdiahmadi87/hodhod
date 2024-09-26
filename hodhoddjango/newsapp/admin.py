from .models import News, Topic, NewsAgency, IFrame, API
from django.contrib import admin

# Register your models here.

admin.site.register(API)
admin.site.register(IFrame)
admin.site.register(NewsAgency)
admin.site.register(Topic)
admin.site.register(News)