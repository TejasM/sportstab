from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

__author__ = 'tmehta'


def login_user(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        type = request.POST['type']
        if type == 'signup':
            user = User.objects.create(username=username, email=username)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('/main')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/login')
            login(request, user)
            return redirect('/main')
    else:
        return render(request, 'login.html')


@login_required
def main_page(request):
    return render(request, 'main.html')