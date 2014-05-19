from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from sportstab.models import VideoPlay, Team

__author__ = 'tmehta'


def login_user(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        post_type = request.POST['type']
        if post_type == 'signup':
            user = User.objects.create(username=username, email=username, first_name=request.POST['first_name'],
                                       last_name=request.POST['last_name'])
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
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
    my_teams = Team.objects.filter(users__in=[request.user.id])
    all_teams = Team.objects.filter(users__in=[request.user.id])
    return render(request, 'main.html', {'my_teams': my_teams, 'all_teams': all_teams})


@csrf_exempt
def save_video(request):
    video = VideoPlay.objects.create()
    video.video.save(request.POST['name'], ContentFile(request.FILES['video']), save=False)
    video.save()


def logouthandler(request):
    logout(request)
    return redirect('/')

