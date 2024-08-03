from django.shortcuts import render, HttpResponse

# Create your views here.
def privacy(requests):
    return render(requests, "privacy.html")

def terms(requests):
    return render(requests, "terms.html")