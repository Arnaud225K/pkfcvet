# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from Marochnik.models import MetallGroup, Metall, MarkaMetall

from headers import ID_MENU_MAROCHNIK

import datetime

#class PriceListAdmin(admin.ModelAdmin):
#	list_filter = ('category',)


class SitemapMarochnikXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.5

    def items(self):
        return Metall.objects.filter(isHidden=False).order_by('id')

    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return "/marka/"+str(ID_MENU_MAROCHNIK)+"/%s/" % obj.id

class SitemapMarkaXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.5

    def items(self):
        return MetallGroup.objects.filter(isHidden=False).order_by('id')


    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return "/marka/"+str(ID_MENU_MAROCHNIK)+"/"+str(obj.position.id)+"/"+str(obj.id)

class SitemapOneMarkaXML(Sitemap):
    #Частота обновления страницы
    changefreq= 'weekly'
    priority = 0.8

    def items(self):
        return MarkaMetall.objects.filter(isHidden=False).order_by('id')


    def lastmod(self, obj):
        return datetime.datetime.now()

    def location(self, obj):
        return "/marka/"+str(ID_MENU_MAROCHNIK)+"/"+str(obj.position.position.id)+"/"+str(obj.position.id)+"/"+str(obj.id)