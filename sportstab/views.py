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

from sportstab.models import Team, Play


@login_required
def view_play(request):
    return None


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
        possible_users = User.objects.filter(~Q(pk__in=team.users.values_list('id', flat=True))).values_list(
            'id', 'first_name', 'last_name')
        return render(request, "sportstab/view_team.html",
                      {'team': team, 'possible_users': possible_users, 'player': player, 'manager': manager})


@login_required
def create_team(request):
    if request.method == "POST":
        team = Team.objects.create(team_name=request.POST['team-name'])
        team.managers.add(request.user)
        team.save()
        action.send(request.user, verb='created team: ' + team.team_name)
        return redirect(reverse('plays:view_team', args=(team.id,)))
    else:
        return render(request, "sportstab/create_team.html")


# TODO -- integrate with login (add a username to the request)
#@login_required
@csrf_exempt
def create_play(request):
    debug = 'Request: ' + str(request) + '. Debug: '
    # Maybe this loop is not needed, saw it online
    for x in range (1,100):
        try:
            user = request.POST['user' % x]
            debug += (user + ' ')
            name = request.POST['name' % x]
            debug += (name + ' ')
            jsonstring = request.POST['jsonstring' % x]
            debug += (jsonstring + ' ')

            # Make the play object
            play_creator = User.objects.get(username=user)
            debug += ('creator ')
            newplay = Play(creator=play_creator,
                           name=name,
                           jsonstring=jsonstring
            )
            newplay.save()
            debug += ('saved_play ')

            # Save the preview image
            filename = user + '.' + name + '.png'
            debug += ('preview ')
            newplay.preview.save(filename, ContentFile(request.FILES['preview' % x].read()))

        except:
            return HttpResponse(debug)

    return HttpResponse('Success')

