from django.conf.urls import patterns, include, url

urlpatterns = patterns('SpecPredlozhenie.views',
    url(r'^$', 'show_specpredlozhenie', {}),
    url(r'^(?P<specpredl_slug>[-\w]+)/$', 'show_specpredlozhenie', {}, 'specpredl'),
)
