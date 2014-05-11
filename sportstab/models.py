from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=400)
    users = models.ManyToManyField(User)


class Play(models.Model):
    name = models.CharField(max_length=400)
    accessible_by = models.ManyToManyField(User)


class VideoPlay(models.Model):
    video = models.FileField(upload_to='video/', null=True)
    play = models.ForeignKey(Play)