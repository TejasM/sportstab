from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class VideoPlay(models.Model):
    video = models.FileField(upload_to='video/', null=True)
    accessible_by = models.ManyToManyField(User)