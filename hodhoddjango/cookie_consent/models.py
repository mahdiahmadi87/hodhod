from django.db import models
from django.contrib.auth.models import User

class CookieConsent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)