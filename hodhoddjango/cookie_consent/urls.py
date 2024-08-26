from django.urls import path
from .views import accept_cookies

urlpatterns = [
    # ... سایر URL ها
    path('accept-cookies/', accept_cookies, name='accept_cookies'),
]