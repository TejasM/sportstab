from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Tag(models.Model):
    tag_name = models.CharField(max_length=300)
    available_by_default = models.BooleanField(default=False)
    team = models.ForeignKey('Team', default=None, null=True)


class Play(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=400)
    tags = models.ManyToManyField(Tag)
    preview = models.ImageField(upload_to='screenshots/', blank=True)
    jsonstring = models.CharField(max_length=10000000, default="")

    def get_tags(self):
        return [(t.id, t.tag_name) for t in self.tags.all()]

    def get_id_tags(self):
        return [t.id for t in self.tags.all()]

    def get_string_tags(self):
        return [t.tag_name for t in self.tags.all()]


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
    preferred_tags = models.ManyToManyField(Tag)

    def get_preferred_tags(self):
        return [(t.id, t.tag_name) for t in self.preferred_tags.all()]


def get_snap_name(instance, filename):
    return 'snapshots/' + instance.play.name + '/' + filename


class Snapshot(models.Model):
    image = models.ImageField(upload_to=get_snap_name)
    annotation = models.CharField(max_length=10000, default="")
    play = models.ForeignKey(Play)


@receiver(post_save, sender=UserProfile)
def my_callback(sender, instance, *args, **kwargs):
    default_tags = ["Offense", "Defense", "Against Zone Defense", "Against Man Defense"]
    for t in default_tags:
        try:
            tag = Tag.objects.get(tag_name=t)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(tag_name=t, available_by_default=True)
        instance.preferred_tags.add(tag)