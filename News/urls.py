# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('News.views',
#     url(r'^$', 'news_all', {}, 'news'),
#     url(r'^(\d+)/$', 'news_all', {}, 'news'),
#     url(r'^(?P<news_slug>[-\w]+)/$', 'news_one', {}, 'news'),

# )



from django.urls import re_path
from . import views 

# app_name = 'news'

# urlpatterns = [
#     re_path(r'^$', views.news_all, name='news_list'),
#     re_path(r'^(?P<page>\d+)/$', views.news_all, name='news_list_paginated'),
#     re_path(r'^(?P<news_slug>[-\w]+)/$', views.news_one, name='news_detail'),
# ]



app_name = 'news'

news_urlpatterns = [
    re_path(r'^$', views.news_all, name='news_list'),
    # On donne un nom différent à l'URL paginée
    re_path(r'^(?P<page>\d+)/$', views.news_all, name='news_list_paginated'), 
    re_path(r'^(?P<news_slug>[-\w]+)/$', views.news_one, name='news_detail'),
]

articles_urlpatterns = [
    re_path(r'^$', views.articles_all, name='articles_list'),
    # On donne un nom différent à l'URL paginée
    re_path(r'^articles/(?P<page>\d+)/$', views.articles_all, name='articles_list_paginated'),
    re_path(r'^articles/(?P<articles_slug>[-\w]+)/$', views.articles_one, name='articles_detail'),
]