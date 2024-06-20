from django.db import models

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
    published = models.CharField(max_length=20, null=True)



    def __str__(self):
        return self.title
    
