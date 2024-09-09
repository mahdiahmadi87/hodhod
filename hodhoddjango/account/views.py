from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from newsapp.models import IFrame, News, NewsAgency
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
import sqlite3



def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('/')
            else:
                return redirect('login')
        else:
            errors = str(form.errors)
            d = {
                "A user with that username already exists.": "حسابی با این نام کاربری قبلا وجود دارد!",
                "The two password fields didn’t match.": "تکرار رمز عبور، اشتباه وارد شده است!",
                "This password is too short. It must contain at least 8 characters.": "رمز عبور کوتاه است، حداقل متشکل از ۸ حرف باید باشد!",
                "This password is too common.": "رمز عبور خیلی رایج است!",
                "This password is entirely numeric.": "رمز عبور کاملا از اعداد است!",
            }
            error = ""
            for key in d.keys():
                if key in errors:
                    error = d[key]
            if error == "":
                error = form.errors
            return render(request, 'signup.html', {'form': form, 'status': error})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'status': True})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, "status": False})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, "status" : True})

def user_logout(request):
    logout(request)
    return redirect('/')

def privacy(requests):
    return render(requests, "privacy.html")

def terms(requests):
    return render(requests, "terms.html")

def csrf_failure(requests, reason=""):
    return redirect('/')

@login_required(login_url='/accounts/login')
def account(requests):
    iframes = IFrame.objects.filter(user=requests.user)
    news = len(News.objects.all())
    newsAgency = len(NewsAgency.objects.all())
    conn = sqlite3.connect('./../userNews.db')
    viewed = conn.execute(f'SELECT newsId from Viewed where username = "{requests.user.username}"')
    viewed = len(viewed.fetchall())
    return render(requests, "account.html", context={"iframes": iframes, "len": len(iframes), "news": news, "newsAgency": newsAgency, "viewed": viewed})