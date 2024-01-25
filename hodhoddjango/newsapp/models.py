from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class News(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=500)
    detail = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        
        return self.title