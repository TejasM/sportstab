from django.contrib.auth.models import User
from django.db import models


class Play(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=400)
    tags = models.CharField(max_length=400, default="")
    preview = models.ImageField(upload_to='screenshots/', blank=True)
    jsonstring = models.CharField(max_length=10000000, default="")

    def get_tags(self):
        return self.tags.split(',')


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


class Tag(models.Model):
    tag_name = models.CharField(max_length=300)
    available_by_default = models.BooleanField(default=False)