# from django.conf.urls import patterns, include, url

# urlpatterns = patterns('portfolio.views',
#     url(r'^(?P<portfolio_slug>[-\w]+)/$', 'show_portfolio', {}, 'portfolio'),
# )


from django.urls import re_path
from . import views

app_name = 'portfolio'

urlpatterns = [
    re_path(r'^(?P<portfolio_slug>[-\w]+)/$', views.show_portfolio, name='portfolio_detail'),
]