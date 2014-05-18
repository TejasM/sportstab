from django.contrib.auth.models import User
from django.db import models


class Play(models.Model):
    name = models.CharField(max_length=400)
    jsonstring = models.CharField(max_length=10000000, default="")


class VideoPlay(models.Model):
    video = models.FileField(upload_to='video/', null=True)
    play = models.ForeignKey(Play)


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=400)
    users = models.ManyToManyField(User)
    manager = models.ForeignKey(User, related_name='coach', default=None, null=True)
    plays = models.ManyToManyField(Play)