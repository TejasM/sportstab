# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def view_play(request):
    return None


@login_required
def create_team(request):
    return None