from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CookieConsent

@require_POST
def accept_cookies(request):
    if request.user.is_authenticated:
        CookieConsent.objects.update_or_create(
            user=request.user,
            defaults={'accepted': True}
        )
    else:
        CookieConsent.objects.update_or_create(
            session_key=request.session.session_key,
            defaults={'accepted': True}
        )
    return JsonResponse({'status': 'success'})