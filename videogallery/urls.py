# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('videogallery.views',
#     url(r'^$', 'videogallery_all', {}, 'sertificats'),
#     url(r'^(\d+)/$', 'videogallery_all', {}, 'sertificats'),
# )


from django.urls import re_path
from . import views

app_name = 'videogallery'

urlpatterns = [
    re_path(r'^$', views.videogallery_all, name='videogallery_list'),
    re_path(r'^(?P<page>\d+)/$', views.videogallery_all, name='videogallery_list_paginated'),
]