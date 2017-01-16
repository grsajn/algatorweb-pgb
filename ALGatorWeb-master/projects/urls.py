# problems

from django.conf.urls import url
from login.views import *
from projects import views

urlpatterns = [
    url(r'^$',         views.projects,  name='index'),
    url(r'^new',       views.newproject,  name='newproject'),
    url(r'^pdetails',  views.pdetails,  name='pdetails'),
    url(r'^adetails',  views.adetails,  name='adetails'),
    url(r'^tdetails',  views.tdetails,  name='tdetails'),
    url(r'^results',   views.results,   name='results'),
    url(r'^logout/$', logout_page, name='logout'),
]
