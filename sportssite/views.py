import json
from actstream import action
from actstream.models import Action
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from sportstab.models import VideoPlay, Team, UserProfile

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
            action.send(request.user, verb='joined Sportstab!')
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
    feeds = Action.objects.all().order_by('-timestamp')[:20]
    return render(request, 'main.html', {'my_teams': my_teams, 'all_teams': all_teams, 'feeds': feeds})


@login_required
def profile_page(request):
    if request.method == "POST":
        form_type = request.POST.get('type', '')
        try:
            request.user.profile
        except:
            UserProfile.objects.create(user=request.user)
        if form_type == 'pic':
            request.user.profile.picture.save(request.user.first_name + '.' + request.user.last_name + '.png',
                                              ContentFile(request.FILES['file'].read()))
            return HttpResponse(json.dumps({"fail": 0, 'link': request.user.profile.picture.name}),
                                content_type='application/json')
        elif form_type == 'update':
            request.user.profile.fav_position = request.POST['fav-pos']
            request.user.profile.affiliation = request.POST['aff']
            request.user.profile.save()
            return HttpResponse(json.dumps({"fail": 0}),
                                content_type='application/json')
        return HttpResponse(json.dumps({"fail": 1}), content_type='application/json')
    return render(request, 'profile.html')


@csrf_exempt
def save_video(request):
    video = VideoPlay.objects.create()
    video.video.save(request.POST['name'], ContentFile(request.FILES['video']), save=False)
    video.save()


def logouthandler(request):
    logout(request)
    return redirect('/')

