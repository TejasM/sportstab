from django.conf.urls import patterns, include, url
from sportstab import views

urlpatterns = patterns('',
                       # Examples:
                       url(r'^view_play/(?P<play_id>\d+)$', views.view_play, name='view_play'),
                       url(r'^create_team/$', views.create_team, name='create_team'),
                       url(r'^create_play/$', views.create_play),
                       url(r'^app_get_play/$', views.app_get_play),
                       url(r'^app_get_tags/$', views.app_get_tags),
                       url(r'^app_set_tags/$', views.app_set_tags),
                       url(r'^add_tag/(?P<play_id>\d+)$', views.add_tag, name='add_tag'),
                       url(r'^add_snapshot/(?P<play_id>\d+)$', views.add_snapshot, name='add_snapshot'),
                       url(r'^remove_snapshot/$', views.remove_snapshot, name='remove_snapshot'),
                       url(r'^update_snapshot/$', views.update_snapshot, name='update_snapshot'),
                       url(r'^remove_tag/(?P<play_id>\d+)$', views.remove_tag, name='remove_tag'),
                       url(r'^view_team/(?P<team_id>\d+)$', views.view_team, name='view_team'),
)
