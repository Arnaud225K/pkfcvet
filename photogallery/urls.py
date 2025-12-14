# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('photogallery.views',
#     url(r'^$', 'photogallery_all', {}, 'sertificats'),
#     url(r'^(\d+)/$', 'photogallery_all', {}, 'sertificats'),
# )


from django.urls import re_path
from . import views 

app_name = 'photogallery'

urlpatterns = [
    re_path(r'^$', views.photogallery_all, name='photogallery_list'),
    re_path(r'^(?P<page>\d+)/$', views.photogallery_all, name='photogallery_list_paginated'),
]