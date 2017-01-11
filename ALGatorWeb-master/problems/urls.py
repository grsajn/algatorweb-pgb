# problems

from django.conf.urls import url
from login.views import *
from problems import views

urlpatterns = [
    url(r'^$',         views.problems,  name='index'),
    url(r'^pdetails',  views.pdetails,  name='pdetails'),
    url(r'^adetails',  views.adetails,  name='adetails'),
    url(r'^tdetails',  views.tdetails,  name='tdetails'),
    url(r'^results',   views.results,   name='results'),
    url(r'^logout/$', logout_page, name='logout'),
]
