from django.conf import settings
from django.db import models
from uuid import uuid4

# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class NewsAgency(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class News(models.Model):
    newsAgency = models.ForeignKey(NewsAgency, on_delete=models.CASCADE)
    id = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=500)
    abstract = models.TextField(null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    link = models.CharField(max_length=1000, null=True)
    published = models.IntegerField(null=True)
    image = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.title
    
class IFrame(models.Model):
    title = models.CharField(max_length=500)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid4)


    def __str__(self):
        return self.user.username + ": " + self.title + ", " + self.token.hex
    

class API(models.Model):
    title = models.CharField(max_length=500)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid4)

    def __str__(self):
        return self.user.username + ": " + self.title + ", " + self.token.hex
    
