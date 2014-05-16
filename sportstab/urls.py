from django.conf.urls import patterns, include, url
from sportstab import views

urlpatterns = patterns('',
                       # Examples:
                       url(r'^(?P<play_id>\d+)$', views.view_play, name='view_play'),
                       url(r'^create_team$', views.create_team, name='create_team'),
)
