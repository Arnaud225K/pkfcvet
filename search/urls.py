# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('search.views',
#                        (r'^results/$', 'results', {'template_name': 'search/results.html'}, 'search_results'),
#                        )



from django.urls import re_path
from . import views

app_name = 'search'

urlpatterns = [
    re_path(r'^results/$', views.results, {'template_name': 'search/results.html'}, name='search_results'),
]