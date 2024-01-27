from django.db import models

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class News(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=500)
    abstract = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    topics = models.ManyToManyField(Topic)
    link = models.CharField(max_length=1000, null=True)
    published = models.CharField(max_length=20, null=True)



    def __str__(self):
        return self.title
    
