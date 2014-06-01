# Create your views here.
import json

from actstream import action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from sportstab.models import Team, Play, Tag, UserProfile


@login_required
def view_play(request, play_id):
    play = Play.objects.get(pk=play_id)
    my_teams = Team.objects.filter(managers__in=[request.user.id])
    available_tags = Tag.objects.filter(available_by_default=True)
    for t in my_teams:
        available_tags = available_tags | Tag.objects.filter(tag_name__contains=t.team_name)
    available_tags = [(t.id, t.tag_name) for t in available_tags]
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    preferred_tags = profile.get_preferred_tags()
    preferred_tags += play.get_tags()
    preferred_tags = list(set(preferred_tags))
    available_tags = [t for t in available_tags if t not in preferred_tags]
    return render(request, 'sportstab/view_play.html', {'play': play, 'available_tags': available_tags,
                                                        'preferred_tags': preferred_tags})


@login_required
def view_team(request, team_id):
    player = False
    manager = False
    try:
        team = Team.objects.get(pk=team_id, users__in=[request.user.id])
        player = True
    except Team.DoesNotExist:
        try:
            team = Team.objects.get(pk=team_id, managers__in=[request.user.id])
            manager = True
        except Team.DoesNotExist:
            return redirect('/main')
    if request.method == "POST":
        ids = request.POST.getlist('players-added[]')
        players = request.POST.get('players', '')
        if players == '':
            throughmodel = team.managers.through
        else:
            throughmodel = team.users.through
        to_add = []
        names = ""
        for player_id in ids:
            user = User.objects.get(pk=player_id)
            names += user.first_name + ' ' + user.last_name + ','
            to_add.append(throughmodel(user_id=player_id, team_id=team.pk))
        names = names[:-1]
        action.send(request.user, verb='added ' + names + ' to ' + team.team_name)
        throughmodel.objects.bulk_create(to_add)
        return HttpResponse(json.dumps({"fail": 0}), content_type='application/json')
    else:
        possible_users = User.objects.filter(~Q(pk__in=team.users.values_list('id', flat=True)) & ~Q(
            pk__in=team.managers.values_list('id', flat=True))).values_list(
            'id', 'first_name', 'last_name')
        return render(request, "sportstab/view_team.html",
                      {'team': team, 'possible_users': possible_users, 'player': player, 'manager': manager})


@login_required
def create_team(request):
    if request.method == "POST":
        team = Team.objects.create(team_name=request.POST['team-name'])
        team.managers.add(request.user)
        Tag.objects.create(team=team,
                           tag_name=str(request.POST[
                                            'team-name'] + ' by ' + request.user.first_name + ' ' + request.user.last_name))
        team.save()
        action.send(request.user, verb='created team: ' + team.team_name)
        return redirect(reverse('plays:view_team', args=(team.id,)))
    else:
        return render(request, "sportstab/create_team.html")


@login_required
@csrf_exempt
def create_play(request):
    try:
        user = request.POST['user']
        name = request.POST['name']
        jsonstring = request.POST['jsonstring']

        # Make the play object
        play_creator = User.objects.get(username=user)
        newplay = Play.objects.create(creator=play_creator,
                                      name=name,
                                      jsonstring=jsonstring
        )

        # Save the preview image
        filename = user + '.' + name + '.png'
        newplay.preview.save(filename, ContentFile(request.FILES['preview'].read()))

        # Add tags

        # Read the json object for the play, which contains tags
        play_obj = json.loads(jsonstring)
        # Get the list of tag IDs
        id_list = play_obj['tags']['IDs']
        state_list = play_obj['tags']['states']
        # For each ID, get the tag and add it to newplay
        i=0
        for id in id_list:
            tag = Tag.objects.get(pk=int(id))
            if state_list[i]:
                newplay.tags.add(tag)
                if tag.team:
                    tag.team.plays.add(newplay)
            i+=1
        newplay.save()

        # Save this action
        action.send(play_creator, verb='created a new play: ' + name)
    except:
        return HttpResponse('Failed')

    return HttpResponse('Success')


@login_required
@csrf_exempt
def app_get_play(request):
    try:
        name = request.POST['play_name']
        play = Play.objects.get(name=name)
        return HttpResponse(play)
    except:
        return HttpResponse('Failed')


@login_required
@csrf_exempt
def app_get_tags(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    try:
        # This returns the tags as a list of (id, name)
        preferred_tags = profile.get_preferred_tags()
        # Make unique
        preferred_tags = list(set(preferred_tags))
        # Convert this to two lists, one for ids one for names
        id_name_lists = map(list, zip(*preferred_tags))
        id_list = id_name_lists[0]
        name_list = id_name_lists[1]
        return HttpResponse(json.dumps({'IDs' : id_list, 'tags': name_list}), content_type='application/json')
    except:
        return HttpResponse('Failed')

@login_required
@csrf_exempt
def app_set_tags(request):
    # This function is incomplete/wrong
    # See create_play and copy that
    try:
        # Get the play name and json object
        name = request.POST['play_name']
        play = Play.objects.get(name=name)
        json_str = request.POST['input_obj']
        tags_obj = json.loads(json_str)
    except:
        return HttpResponse('Failed')

    try:
        # Get the list of tag IDs
        id_list = tags_obj['IDs']
        # For each ID, get the tag and add it to play
        # COPIED FROM add_tag. Can re-factor into def.
        for id in id_list:
            tag = Tag.objects.get(pk=int(id))
            if tag not in play.tags.all():
                play.tags.add(tag)
                if tag.team:
                    tag.team.plays.add(play)
        play.save()
        return HttpResponse('Success')
    except:
        return HttpResponse('Failed')

@csrf_exempt
def add_tag(request, play_id):
    play = Play.objects.get(pk=play_id)
    tag = Tag.objects.get(pk=int(request.POST['id']))
    if tag not in play.tags.all():
        play.tags.add(tag)
        if tag.team:
            tag.team.plays.add(play)
    play.save()
    return HttpResponse(json.dumps({'fail': 0}), content_type='application/json')


@csrf_exempt
def remove_tag(request, play_id):
    play = Play.objects.get(pk=play_id)
    tag = Tag.objects.get(pk=int(request.POST['id']))
    if tag in play.tags.all():
        play.tags.remove(tag)
        if tag.team and play in tag.team.plays.all():
            tag.team.plays.remove(play)
    play.save()
    return HttpResponse(json.dumps({'fail': 0}), content_type='application/json')
