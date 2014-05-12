from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from sportstab.models import VideoPlay

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
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/teams')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/login')
            login(request, user)
            
            # TODO:
            # If they have any teams, redirect to main
            # Otherwise redirect to teams
            
            return redirect('/main')
    else:
        return render(request, 'login.html')


@login_required
def main_page(request):
    return render(request, 'main.html')


@login_required
def teams_page(request):
    return render(request, 'teams.html')


@csrf_exempt
def save_video(request):
    video = VideoPlay.objects.create()
    video.video.save(request.POST['name'], ContentFile(request.FILES['video']), save=False)
    video.save()

def logoffhandler(request):
	logout(request)
	redirect_url = request.GET.get("redirect","/")
	return redirect(redirect_url)

