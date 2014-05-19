from django.contrib.auth.models import User
from django.db import models


class Play(models.Model):
    name = models.CharField(max_length=400)
    tags = models.CharField(max_length=400)
    preview = models.FileField(upload_to='screenshots/', null=True)
    jsonstring = models.CharField(max_length=10000000, default="")


class VideoPlay(models.Model):
    video = models.FileField(upload_to='video/', null=True)
    play = models.ForeignKey(Play)


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=400)
    users = models.ManyToManyField(User, related_name='players')
    managers = models.ManyToManyField(User, related_name='coach')
    plays = models.ManyToManyField(Play)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    fav_position = models.CharField(max_length=100, default='All Positions')
    affiliation = models.CharField(max_length=1000, default="")
    picture = models.ImageField(upload_to='user_pics/', blank=True)
