# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

import datetime

from News.models import News

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class SitemapNewsXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.9

    def items(self):
        return News.objects.filter(isHidden=False).order_by('id')

    def lastmod(self, obj):
        return  datetime.datetime.now()

    def location(self, obj):
        return "/news/%s/" % obj.id
