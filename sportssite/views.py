import json
import logging

from actstream import action
from actstream.models import Action
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import requests

from sportstab.models import VideoPlay, Team, UserProfile, Play, Tag


__author__ = 'tmehta'

logger = logging.getLogger(__name__)


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
            r = requests.get('https://auth.firebase.com/auth/firebase/create',
                             params={'firebase': 'esc472sportstab', 'email': username, 'password': password,
                                     'transport': 'json'})
            logger.debug(r)
            return redirect('/main')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/login')
            login(request, user)
            return redirect('/main')
    else:
        return render(request, 'login.html')


@csrf_exempt
def app_checkusername(request):
    if request.method == 'POST':
        username = request.POST['email'].strip()
        # Check if username available
        try:
            user = User.objects.get(username=username)
            return HttpResponse("USERNAME_EXISTS")
        except:
            pass
        return HttpResponse("OKAY")


@csrf_exempt
def app_login_user(request):
    try:
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
            return HttpResponse('Success')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/login')
            login(request, user)
            return HttpResponse('Success')
    except:
        return HttpResponse('Failed')


@login_required
def main_page(request):
    my_teams = Team.objects.filter(Q(users__in=[request.user.id]) | Q(managers__in=[request.user.id]))
    tags = None
    if my_teams:
        tags = Tag.objects.filter(tag_name__contains=my_teams[0].team_name)
        for t in my_teams:
            tags = Tag.objects.filter(tag_name__contains=t.team_name) | tags
    plays = None
    if tags:
        plays = Play.objects.filter(tag__in=list(tags))
    all_teams = Team.objects.all()
    feeds = Action.objects.all().order_by('-timestamp')[:20]
    return render(request, 'main.html',
                  {'my_teams': my_teams, 'all_teams': all_teams, 'feeds': feeds, 'user': request.user,
                   'plays': plays})


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

