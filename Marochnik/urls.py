# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('Marochnik.views',
#     url(r'^top/(?P<metall_slug>[-\w]+)/$', 'show_metall', {}, 'metall'),
#     url(r'^cat/(?P<metall_group_slug>[-\w]+)/$', 'show_metall_group', {}, 'metall_group'),
#     url(r'^(?P<marka_metall_slug>[-\w]+)/$', 'show_marka_metall', {}, 'marka_metall'),
#     # url(r'^marka/(\d+)/(\d+)/(\d+)/$', MetallGroupV),
#     # url(r'^marka/(\d+)/(\d+)/(\d+)/(\d+)/$', MarkaV),
# )



from django.urls import re_path
from . import views

app_name = 'marochnik'

urlpatterns = [    
    re_path(r'^top/(?P<metall_slug>[-\w]+)/$', views.show_metall, name='metall_detail'),
    re_path(r'^cat/(?P<metall_group_slug>[-\w]+)/$', views.show_metall_group, name='metall_group_detail'),
    re_path(r'^(?P<marka_metall_slug>[-\w]+)/$', views.show_marka_metall, name='marka_metall_detail'),
]