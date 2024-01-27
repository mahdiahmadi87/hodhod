from .models import News, Tag, Topic, NewsAgency

def fromDbToDjango(newsAgency):
    print(NewsAgency.objects.all().values())
