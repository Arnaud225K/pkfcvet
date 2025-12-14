# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('Sertificats.views',
#     url(r'^$', 'sertficats_all', {}, 'sertificats'),
#     url(r'^(\d+)/$', 'sertficats_all', {}, 'sertificats'),
# )



from django.urls import re_path
from . import views

app_name = 'sertificats'

urlpatterns = [
    re_path(r'^$', views.sertficats_all, name='sertificats_list'),
    re_path(r'^(?P<page>\d+)/$', views.sertficats_all, name='sertificats_list_paginated'),
]