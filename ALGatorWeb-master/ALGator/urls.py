# ALGator/urls.py

from django.conf.urls import patterns, include, url

from login.views import *
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),  # If user is not logged in, redirect to login
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^guest/$',guest),
    url(r'^home/$', home),
    url(r'^settings/$', settings_page),
    url(r'^cpanel/', (include('cpanel.urls', namespace='cpanel'))),
    url(r'^vision/', include('vision.urls', namespace='vision'))

)

