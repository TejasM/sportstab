# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from sportstab.models import Team


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
            team = Team.objects.get(pk=team_id, manager__in=[request.user.id])
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
        for player_id in ids:
            to_add.append(throughmodel(user_id=player_id, team_id=team.pk))
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
        return redirect(reverse('plays:view_team', args=(team.id,)))
    else:
        return render(request, "sportstab/create_team.html")