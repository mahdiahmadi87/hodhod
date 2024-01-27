from django.contrib import admin
from .models import News, Tag, Topic

# Register your models here.

admin.site.register(News)
admin.site.register(Tag)
admin.site.register(Topic)
