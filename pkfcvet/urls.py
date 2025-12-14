import os
from django.contrib import admin
from django.urls import re_path, path, include
from django.conf import settings
from django.conf.urls.static import static
import logging
from Export import views as export_views
from import_control.views import import_control_url
# from News.views import articles_all, articles_one
from .views import RobotsV, clear_session, catalog_update, SendFormOrder, sitemap_gen
from django.views.static import serve
from News.urls import news_urlpatterns, articles_urlpatterns
logger = logging.getLogger(__name__)


admin.autodiscover()

handler404 = 'menu.views.handler404'
handler500 = 'menu.views.handler500'


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin_m/', include('admin_m.urls')),
]

#Activate debug toolbar url
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

urlpatterns += [
    # path('admin/', admin.site.urls),
    # path('admin/doc/', include('django.contrib.admindocs.urls')),
    # path('admin_m/', include('admin_m.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('search/', include('search.urls')),
    # path('news/', include('News.urls')),
    path('news/', include((news_urlpatterns, 'news'), namespace='news')),
    # Section Articles
    path('articles/', include((articles_urlpatterns, 'news'), namespace='articles')),
    path('sertificats/', include('Sertificats.urls')),
    path('photogallery/', include('photogallery.urls')),
    path('videogallery/', include('videogallery.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('gost/', include('GOST.urls')),
    path('marka/', include('Marochnik.urls')),
    re_path(r'^robots.txt$', RobotsV),
    path('sitemap_gen/', sitemap_gen),
    path('catalog_update/', catalog_update),
    path('export/', export_views.ExportViews),
    path('catalog_export/', export_views.ExportCatalog),
    #path('orderphone_new/', OrderPhone),
    path('orderphone_new/', SendFormOrder.as_view(), name='send_form_order'),
    path('clear_session/', clear_session),
    path('import_control/', import_control_url),
    path('', include('menu.urls')),
]

#Serve static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)	
urlpatterns += [
        re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.WWW_ROOT}),
    ]

if hasattr(settings, 'WWW_ROOT') and settings.WWW_ROOT and os.path.isdir(settings.WWW_ROOT):
    sitemap_root_pattern = r'^(?P<path>sitemap(?:_[\w\.-]*)?\.xml(?:\.gz)?)$'
    urlpatterns += [
        re_path(sitemap_root_pattern, serve, {'document_root': settings.WWW_ROOT}),
    ]
else:
    logger.warning(f"Settings.WWW_ROOT ('{getattr(settings, 'WWW_ROOT', 'Not Set')}') is not a valid directory. Sitemaps at root won't be served by runserver.")