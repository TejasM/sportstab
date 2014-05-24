from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView
from sportssite.views import app_login_user, login_user, main_page, logouthandler, profile_page

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', view=TemplateView.as_view(template_name='index.html')),
                       # url(r'^sportssite/', include('sportssite.foo.urls')),
                       url(r'^login/', login_user),
                       url(r'^app_login$', app_login_user),
                       url(r'^main/', main_page),
                       url(r'^profile/', profile_page),
                       url(r'^plays/', include('sportstab.urls', namespace='plays')),
                       url(r'^logout$', logouthandler),
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url('^activity/', include('actstream.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
