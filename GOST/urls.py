# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('GOST.views',
#     url(r'^(?P<gost_slug>[-\w]+)/$', 'show_gost', {}, 'gost'),
# )


from django.urls import re_path
from . import views

app_name = 'gost'

urlpatterns = [
    re_path(r'^(?P<gost_slug>[-\w]+)/$', views.show_gost, name='gost_detail'),
]